import datetime
from typing import Optional, List, Dict, Any

class MQTTManager:
    """
        Zarządza połączeniem z brokerem MQTT, subskrypcjami i odbiorem wiadomości
        z Modułu Symulacji Środowiska.
        """

    def __init__(self, broker_url: str, topics: List[str]):
        self.broker_url = broker_url
        self.topics = topics
        self.connection_status = False

    def connect(self) -> bool:
        """
        Nawiązuje połączenie z brokerem MQTT.
        """
        self.connection_status = True
        print(f"MQTT: Połączono z brokerem na {self.broker_url}")

        for topic in self.topics:
            self.subscribe(topic)

        return self.connection_status

    def reconnect(self) -> bool:
        """
        Automatycznie ponawia próbę połączenia.
        Wymagane, aby moduł automatycznie odzyskiwał połączenie po awarii MQTT.
        """
        if not self.connection_status:
            print("MQTT: Trwa ponawianie połączenia...")
            self.connection_status = self.connect()

        return self.connection_status

    def get_connection_status(self) -> bool:
        """
        Zwraca bieżący stan połączenia.
        """
        return self.connection_status

    def subscribe(self, topic: str) -> None:
        """
        Subskrybuje określony temat.
        """

        print(f"MQTT: Subskrybowano temat: {topic}")

    def receive(self) -> Optional[Dict[str, Any]]:
        """
        Odbiera surową wiadomość MQTT (JSON/dict) i zwraca ją do HandleData.
        Symuluje odbiór danych z Modułu Symulacji Środowiska.
        """
        if not self.connection_status:
            return None

        raw_message = {
            'sensor_id': 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'value': 21.3,
            'unit': 'C'
        }

        return raw_message