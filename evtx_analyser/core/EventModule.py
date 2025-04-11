from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class EventModule(ABC):
    def __init__(self):
        self.ns = {'e': 'http://schemas.microsoft.com/win/2004/08/events/event'}
        
    @property
    @abstractmethod
    def name(self) -> str :
        """Each module must define a name"""
        pass
    
    @property
    @abstractmethod
    def eventID(self) -> str :
        """event ID of the module"""   
        pass
    
    @property
    @abstractmethod
    def group(self) -> str :
        """Each module must be part of a group of module."""
        pass
    
    @property
    @abstractmethod
    def xpaths(self) -> list[str] :
        """xpaths to extract data from the event"""
        pass
    
    @abstractmethod
    def clean_event_data(self, raw_event_datas) -> str :
        return raw_event_datas

    def parse_event_data(self, evtx_event) :
        # print(evtx_event)
        root = ET.fromstring(evtx_event)
        raw_event_datas = []
        
        for xpath in self.xpaths:
            elements = root.findall(xpath, self.ns)
            raw_event_datas.append(elements)

        return self.clean_event_data(raw_event_datas)