from abc import ABC
from base.device import Device
from base.environment import Environment


class SmartDevice(Device, ABC):
    power_usage: float
    
    def __init__(self, name: str, env: Environment, power_usage_watt: float):
        if type(self) is SmartDevice:
            raise TypeError("SmartDevice is abstract")
        
        super().__init__(name, env)
        self.power_usage = power_usage_watt

    def get_power_usage(self, millis_passed: int) -> float:
        if not self.is_active:
            return 0.0

        hours = millis_passed / 3600000
        return (self.power_usage * hours) / 1000.0
