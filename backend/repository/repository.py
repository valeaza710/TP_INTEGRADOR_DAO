from abc import ABC, abstractmethod
from pywin.mfc.object import Object

class Repository(ABC):
    @abstractmethod
    def save(self, objeto:Object):
        pass

    @abstractmethod
    def get_by_id(self, id:int) -> Object:
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def modify(self, objeto:Object) -> Object:
        pass

    @abstractmethod
    def delete(self, objeto:Object):
        pass
