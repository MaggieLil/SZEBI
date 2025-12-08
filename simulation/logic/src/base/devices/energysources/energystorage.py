from devices.energysource import EnergySource
from base.weather import Weather
from base.environment import Environment

class EnergyStorage(EnergySource):
    def __init__(self, name: str, env: Environment, capacity_kwh: float, max_charge_kw: float, max_discharge_kw: float) -> None:
        super().__init__(name, env)
        self.capacity = capacity_kwh
        self.charge = 0.0
        self.max_charge = max_charge_kw
        self.max_discharge = max_discharge_kw

    def charge_battery(self, energy_kwh: int) -> float:
        accepted = min(self.capacity - self.charge, self.max_charge, energy_kwh)
        self.charge += accepted
        return accepted

    def discharge_battery(self, needed_kwh: int) -> float:
        provided = min(self.charge, self.max_discharge, needed_kwh)
        self.charge -= provided
        return provided

    def calculate_production(self, weather: Weather, millis_passed: int) -> float:
        return 0.0