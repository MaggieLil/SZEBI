from abc import abstractmethod, ABC
from uuid import UUID, uuid4
from src.base.environment import Environment
from src.base.simulation import Simulation
from src.util.utils import validate_name
import weakref

class Device(ABC):
    uuid: UUID = uuid4()
    is_active: bool = False
    
    def __init__(self, name: str, environment: Environment) -> None:
        if type(self) is Device:
            raise TypeError("Device is abstract")
        
        self._environment = weakref.ref(environment)
        self._simulation = weakref.ref(environment.sim())

        self.set_name(name)

    def enable(self) -> None:
        if self.is_active:
            raise ValueError('device is already enabled')
        self.is_active = True

    def disable(self) -> None:
        if not self.is_active:
            raise ValueError('device is already disabled')
        self.is_active = False

    def env(self) -> Environment:
        e = self._environment() 
        if e is None:
            raise RuntimeError('Device exists outside of Environment context')
        return e

    def sim(self) -> Simulation:
        s = self._simulation() 
        if s is None:
            raise RuntimeError('Weather exists outside of Simulation context')
        return s

    @abstractmethod
    def update(self, millis_passed: int) -> None:
        pass

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        validate_name(name)
        self.name = name



