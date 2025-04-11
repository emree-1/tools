import re

from core.EventModule import EventModule
from utils.languages import language_mapping
from utils.exit_status import exit_status

class Event1033Module(EventModule):
    @property
    def name(self) -> str: return "Event ID 1033"
    @property
    def eventID(self) -> str: return "1033"
    @property
    def group(self) -> str: return "msi_install"
    @property
    def xpaths(self) -> list[str] : return [
            "e:EventData/e:Data",
            "e:EventData/e:Binary" # Binary data not used, but can be useful in the future
        ]
    
    def clean_event_data(self, raw_event_datas) -> str:
        cleaned_data = re.sub(r'<string>\(NULL\)</string>|<string></string>', '', raw_event_datas[0][0].text)
        cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()
        elements = re.findall(r'<string>(.*?)</string>', cleaned_data)
        return f"{elements[0]} ({elements[1]}) | {elements[4]} | {language_mapping.get(elements[2], 'Unknown')} | {exit_status.get(elements[3], 'Unknown')}", elements