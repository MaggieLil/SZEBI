from typing import Dict

from .validator import Validator
from .deduplicator import Deduplicator
from .transformer import Transformer
from ..logic.database_manager import DatabaseManager

from ..models import Measurement, DataLog, MeasurementStatus, DataLogLevel


class HandleData:
    def __init__(self, db_manager: DatabaseManager):
        self.validator = Validator()
        self.deduplicator = Deduplicator()
        self.transformer = Transformer()
        self.db_manager = db_manager

    def _convert_raw_to_measurements(self, raw_data: Dict) -> Measurement:
        """
        Transformacja wiadomości MQTT z formatu JSON do obiektów wewnętrznych systemu.
        """

        sensor_stub = self.db_manager.get_sensor(raw_data.get('sensor_id'))

        measurement = Measurement(
            sensor=sensor_stub,
            timestamp=raw_data.get('timestamp'),
            value=raw_data.get('value'),
            status=MeasurementStatus.OK
        )
        return measurement

    def process(self, raw_data: Dict) -> Measurement:
        """
        Główna metoda przetwarzania danych (process(in data: Measurement) Measurement).
        """
        try:
            measurement = self._convert_raw_to_measurement(raw_data)
        except Exception as e:
            log = DataLog(level=DataLogLevel.CRITICAL, message=f"Failed conversion: {e}", measurement=None)
            self.db_manager.insert_data_log(log)
            return None

        # Walidacja
        if not self.validator.validate(measurement):
            measurement.status = MeasurementStatus.ERROR
            log = DataLog(level=DataLogLevel.ERROR, message="Validation failed", measurement=measurement)
            self.db_manager.insert_data_log(log)
            self.db_manager.insert_measurements(measurement)
            return measurement

        # Deduplikacja
        if self.deduplicator.merge_duplicates(measurement):
            measurement.status = MeasurementStatus.DUPLICATE
            log = DataLog(level=DataLogLevel.INFO, message="Duplicate found", measurement=measurement)
            self.db_manager.insert_data_log(log)
            self.db_manager.insert_measurements(measurement)
            return measurement

        # Normalizacja jednostek
        measurement = self.transformer.convert_units(measurement)
        measurement.status = MeasurementStatus.OK

        # Zapis do bazy i aktualizacja czujnika
        self.db_manager.insert_measurements(measurement)
        self.db_manager.update_sensor(measurement.sensor.pk, measurement.timestamp)

        return measurement