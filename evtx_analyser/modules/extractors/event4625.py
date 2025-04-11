from core.EventModule import EventModule
from utils.logon_types import logon_types
class Event4625Module(EventModule):
    @property
    def name(self) -> str: return "Event ID 4625"
    @property
    def eventID(self) -> str: return "4625"
    @property
    def group(self) -> str: return "msi_install"
    @property
    def xpaths(self) -> list[str] : return [
        "e:EventData/e:Data"
        ]
    
    def clean_event_data(self, raw_event_datas) -> str:
        elements = [element.text for element in raw_event_datas[0]]
        return f"Login attempt failed", elements