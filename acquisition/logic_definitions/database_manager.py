import datetime
from typing import List, Optional
from ..models import Measurement, DataLog, Sensor, SensorStatus

class DatabaseManager:
    """
    Klasa DatabaseManager obsługuje wszystkie interakcje modułu akwizycji
    z bazą danych PostgreSQL.
    """
    def __init__(self):
        self.db_connection = None

    def insert_measurements(self, measurement: Measurement) -> None:
        """
        Zapisuje zwalidowane/oznaczone dane pomiarowe do tabeli measurements.
        """
        print(
            f"DB: INSERT MEASUREMENT: Sensor {measurement.sensor.pk}, Value: {measurement.value}, Status: {measurement.status}")

    def insert_data_log(self, log: DataLog) -> None:
        """
        Rejestruje błędy walidacji, połączenia lub przetwarzania w tabeli data_logs.
        """
        print(f"DB: INSERT DATA_LOG: Level: {log.level}, Message: {log.message[:30]}...")

    def update_sensor(self, sensor_id: int, timestamp: datetime.datetime) -> None:
        """
        Aktualizuje last_communication w tabeli sensors.
        """
        print(f"DB: UPDATE SENSOR {sensor_id}: last_communication updated to {timestamp}")

    def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        """
        Pobiera obiekt Sensor na podstawie sensor_id. Stub: zwraca fikcyjny obiekt.
        """
        print(f"DB: GET SENSOR {sensor_id}: Fikcyjny obiekt zwrócony.")

        return Sensor(
            pk=sensor_id,
            name=f"Sensor-{sensor_id}",
            status=SensorStatus.ACTIVE
        )

    def get_measurements(self, sensor_id: int, start: datetime.datetime, end: datetime.datetime) -> List[Measurement]:
        """
        Pobiera listę pomiarów z danego zakresu czasu dla modułów Prognozowania/Analizy.
        """
        return []

    def get_logs(self, level: str) -> List[DataLog]:
        """
        Pobiera logi błędów według poziomu (np. ERROR) dla Administratora.
        """
        return []

    def get_sensor_statistics(self) -> list:
        """
        Pobiera statystyki czujników (do Monitorowania).
        """
        return []