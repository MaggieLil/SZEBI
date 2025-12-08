from devices.energysource import EnergySource
from base.weather import Weather
from base.environment import Environment


class ElectricGrid(EnergySource):
    def __init__(self, env: Environment, price_per_kwh: float = 0.8):
        super().__init__("electric-grid", env)
        self.price_per_kwh = price_per_kwh

    def calculate_production(self, weather: Weather, millis_passed: int) ->float:
        return 0.0

    def update(self, millis_passed: int) -> None:
        pass

    def supply(self, needed_kwh: float)->float:
        return needed_kwh