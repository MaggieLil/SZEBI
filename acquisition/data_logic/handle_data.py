import datetime
from typing import Dict, Optional

from .validator import Validator
from .deduplicator import Deduplicator
from .transformer import Transformer
from ..logic.database_manager import DatabaseManager

from ..models import Measurement, DataLog, MeasurementStatus, DataLogLevel, Location, SensorType, Sensor


class HandleData:
    def __init__(self, db_manager: DatabaseManager, validator: Validator, deduplicator: Deduplicator, transformer: Transformer):
        self.validator = validator
        self.deduplicator = deduplicator
        self.transformer = transformer
        self.db_manager = db_manager

    def process(self, raw_data: Dict) -> Optional[Measurement]:
        """
        Główna metoda przetwarzania danych. Przyjmuje słownik zawierający
        kontekst (UUID, parametr) i wartość.
        """
        try:
            # 1. Konwersja i mapowanie kontekstu
            measurement = self._convert_raw_to_measurement(raw_data)
            if measurement is None:
                return None

        except Exception as e:
            log = DataLog(level=DataLogLevel.CRITICAL, message=f"KRYTYCZNY BŁĄD KONWERSJI/MAPOWANIA: {e}",
                          measurement=None)
            self.db_manager.insert_data_log(log)
            return None

        # 2. Walidacja
        if not self.validator.validate(measurement):
            measurement.status = MeasurementStatus.ERROR
            log = DataLog(level=DataLogLevel.ERROR, message="Walidacja nie powiodła się (poza limitem)",
                          measurement=measurement)
            self.db_manager.insert_data_log(log)
            self.db_manager.insert_measurements(measurement)
            return measurement

        # 3. Deduplikacja (i ewentualne scalenie)
        if self.deduplicator.merge_duplicates(measurement):
            measurement.status = MeasurementStatus.DUPLICATE
            log = DataLog(level=DataLogLevel.INFO, message="Wykryto duplikat", measurement=measurement)
            self.db_manager.insert_data_log(log)
            self.db_manager.insert_measurements(measurement)
            return measurement

        # 4. Normalizacja i finalny status
        # measurement = self.transformer.convert_units(measurement)
        measurement.status = MeasurementStatus.OK

        # 5. Zapis do bazy i aktualizacja czujnika
        self.db_manager.insert_measurements(measurement)
        self.db_manager.update_sensor(measurement.sensor.pk, measurement.timestamp)

        return measurement

    def _convert_raw_to_measurement(self, raw_data: Dict) -> Optional[Measurement]:
        """
        Transformuje surowe dane (z kontekstem UUID i param_name) na obiekt Measurement.
        """
        try:
            sensor = self._find_or_create_sensor(
                raw_data['location_uuid'],
                raw_data['param_name']
            )

            measurement = Measurement(
                sensor=sensor,
                timestamp=datetime.datetime.fromisoformat(raw_data['timestamp']),
                value=raw_data['value'],
                status=MeasurementStatus.OK
            )
            return measurement

        except Exception as e:
            raise e

    def _find_or_create_sensor(self, location_uuid: str, param_name: str) -> Sensor:
        """
        Znajduje Sensor na podstawie kontekstu (Location + SensorType) lub go tworzy.
        """

        sensor_type = self._get_sensor_type(param_name)
        location = self._get_or_create_location(location_uuid)

        sensor, created = Sensor.objects.get_or_create(
            location=location,
            sensor_type=sensor_type,
            defaults={
                'name': f"{sensor_type.name} w {location.room}"
            }
        )

        if created:
            self.db_manager.insert_data_log(DataLog(
                level=DataLogLevel.INFO,
                message=f"Utworzono nowy Sensor: {sensor.name}"
            ))

        return sensor

    def _get_or_create_location(self, location_uuid: str) -> Location:
        """
        Znajduje istniejącą lokalizację po UUID lub tworzy nową z domyślną nazwą.
        """
        location, created = Location.objects.get_or_create(
            room=location_uuid,
            defaults={
                'room': f"{location_uuid[:8]}"
            }
        )

        if created:
            self.db_manager.insert_data_log(DataLog(
                level=DataLogLevel.INFO,
                message=f"Utworzono nową Lokalizację: {location.room}. Wymagana weryfikacja nazwy."
            ))

        return location

    def _get_sensor_type(self, param_name: str) -> SensorType:
        """
        Pobiera SensorType na podstawie nazwy parametru z tematu MQTT.
        """
        return SensorType.objects.get(name__iexact=param_name)