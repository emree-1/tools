from core.EventModule import EventModule
import re

class Event11707Module(EventModule):
    @property
    def name(self) -> str: return "Event ID 11707"
    @property
    def eventID(self) -> str: return "11707"
    @property
    def group(self) -> str: return "msi_install"
    @property
    def xpaths(self) -> list[str] : return [
            "e:EventData/e:Data"
        ]
    
    def clean_event_data(self, raw_event_datas) -> str:    
        cleaned_data = re.sub(r'<string>\(NULL\)</string>', '', raw_event_datas[0]) 
        cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()
        cleaned_data = re.sub(r'<string></string>', '', cleaned_data)  
        return  re.findall(r'<string>(.*?)<\/string>', cleaned_data)[0]