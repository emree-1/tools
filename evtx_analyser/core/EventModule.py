from abc import ABC, abstractmethod

class EventModule(ABC):
    @property
    @abstractmethod
    def name(self):
        """Each module must define a name"""
        pass
    
    @property
    @abstractmethod
    def group(self):
        """Each module must be part of a group of module."""
        pass
    
    @abstractmethod
    def parse(self, evtx_event) :
        pass
    
    @abstractmethod
    def match(self, evtx_event) -> bool:
        pass
    
    @abstractmethod
    def analyze(self, evtx_event) -> dict:
        pass
