import time
import threading
import os
from django.apps import AppConfig
from django.conf import settings

from .logic.MQTT_manager import MQTTManager
from .data_logic.handle_data import HandleData
from .logic.database_manager import DatabaseManager
from .data_logic.validator import Validator
from .data_logic.deduplicator import Deduplicator
from .data_logic.transformer import Transformer

from .models import DataLog, DataLogLevel


class AcquisitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acquisition'

    def ready(self):
        """
        Metoda wywoływana automatycznie po załadowaniu aplikacji Django.
        Uruchamia Worker MQTT w osobnym wątku.
        """
        if os.environ.get('RUN_MAIN') or settings.DEBUG and os.environ.get('DJANGO_SETTINGS_MODULE'):
            worker_thread = threading.Thread(target=self._run_mqtt_worker, daemon=True)
            worker_thread.start()
            print("INFO: MQTT Worker (Akwizycja Danych) został uruchomiony w tle.")

    def _run_mqtt_worker(self):
        """
        Logika pętli akwizycji. Działa w osobnym wątku.
        """
        # 1. INICJALIZACJA WSZYSTKICH ZALEŻNOŚCI
        db_manager = DatabaseManager()
        validator = Validator()
        deduplicator = Deduplicator()
        transformer = Transformer()

        # Inicjalizacja Głównego Handlera, przekazując wszystkie zależności
        data_handler = HandleData(
            db_manager=db_manager,
            validator=validator,
            deduplicator=deduplicator,
            transformer=transformer
        )

        # Konfiguracja MQTT (mock do integracji)
        mqtt_manager = MQTTManager(
            broker_url="localhost:1883",
            topics=["environment/#"]
        )

        # 2. GŁÓWNA PĘTLA NASŁUCHIWANIA
        try:
            if mqtt_manager.connect():
                while mqtt_manager.get_connection_status():

                    # symulacja odbioru danych z MQTT (receive())
                    raw_messages = mqtt_manager.receive()

                    if raw_messages:
                        for message in raw_messages:
                            data_handler.process(message)

                    time.sleep(1)


        except Exception as e:
            error_message = f"KRYTYCZNY BŁĄD WORKER: {e}. Proces akwizycji zatrzymany."
            print(error_message)

            try:

                log = DataLog(
                    level=DataLogLevel.CRITICAL,
                    message=error_message
                )

                db_manager.insert_data_log(log)

            except Exception as log_e:
                print(f"BŁĄD ZAPISU LOGU KRYTYCZNEGO: Nie można zapisać logu do bazy: {log_e}")