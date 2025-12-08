from ..smartdevice import SmartDevice
from base.environment import Environment

class AirConditioning(SmartDevice):
    def __init__(self, name: str, env: Environment, power_usage_watt: float, target_temp: float = 24):
        super().__init__(name, env, power_usage_watt)
        self.target_temp = target_temp
        self.is_cooling = False

    def update(self, millis_passed: int):
        if not self.is_active:
            self.is_cooling = False
            return

        if self.env().weather.get_temperature() > self.target_temp:
            self.is_cooling = True
            self.env().weather.apply_cooling(self.power_usage)
        else:
            self.is_cooling = False

    def get_power_usage(self, millis_passed: int) -> float:
        if not self.is_active or not self.is_cooling:
            return 0.0
        return super().get_power_usage(millis_passed)
