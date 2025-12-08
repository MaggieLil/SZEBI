from ..smartdevice import SmartDevice
from base.environment import Environment


class Heating(SmartDevice):
    def __init__(self, name: str, env: Environment, power_usage_watt: float, target_temp: float = 21.0):
        super().__init__(name, env, power_usage_watt)
        self.target_temp = target_temp
        self.is_heating = False

    def update(self, millis_passed: int):
        if not self.is_active:
            self.is_heating = False
            return

        if self.env().weather.get_temperature() < self.target_temp:
            self.is_heating = True
            self.env().weather.apply_heating(self.power_usage)
        else:
            self.is_heating = False

    def get_power_usage(self, millis_passed: int) -> float:
        if not self.is_active or not self.is_heating:
            return 0.0
        return super().get_power_usage(millis_passed)
