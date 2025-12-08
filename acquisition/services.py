import datetime
from typing import List, Optional, Dict, Any

from .logic.database_manager import DatabaseManager
from .models import Measurement, DataLog

class AcquisitionDataService:
    """
    Warstwa Usługowa: Publiczne API Modułu Akwizycji dla innych modułów SZEBI.
    Umożliwia pobieranie danych historycznych, bieżącego stanu sensorów i logów.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_measurements_by_time_range(
        self,
        sensor_id: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime
    ) -> List[Measurement]:
        """
        [API Read Method 1] Pobiera wszystkie pomiary dla danego czujnika
        w określonym zakresie czasu.
        """
        return self.db_manager.get_measurements(sensor_id, start_time, end_time)

    def get_latest_measurement(self, sensor_id: int) -> Optional[Measurement]:
        """
        [API Read Method 2] Pobiera najnowszy, pojedynczy pomiar dla czujnika.
        """
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=1)

        latest_list = self.db_manager.get_measurements(sensor_id, start_time, end_time)
        return latest_list[-1] if latest_list else None


    def get_sensor_statistics(self) -> List[Dict[str, Any]]:
        """
        [API Read Method 3] Pobiera statystyki czujników.
        Używane przez Moduł Monitorowania.
        """
        return self.db_manager.get_sensor_statistics()

    def get_logs_by_level(self, level: str) -> List[DataLog]:
        """
        [API Read Method 4] Pobiera logi błędów wg poziomu.
        """
        return self.db_manager.get_logs(level)