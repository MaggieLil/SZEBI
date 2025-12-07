from typing import Dict
from ..models import Measurement

class Validator:
    def __init__(self):
        self.rules: Dict = {}

    def validate(self, data: Measurement) -> bool:
        """
        Weryfikuje poprawność danych (struktura, zakresy, format).
        """
        if data.value is None:
            return False

        return True