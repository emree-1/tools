from core.EventModule import EventModule
from utils.logon_types import logon_types

class Event4624Module(EventModule):
    @property
    def name(self) -> str: return "Event ID 4624"
    @property
    def eventID(self) -> str: return "4624"
    @property
    def group(self) -> str: return "msi_install"
    @property
    def xpaths(self) -> list[str] : return [
        "e:EventData/e:Data"
        ]
    
    # Dictionnaire de fonctions de description avec fonctions inline
    description_functions = {
        "Interactive": lambda e: f"Interactive Login | Target SID: {e[4]}",
        "Network": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "Batch": lambda e: f"Network Login | Target SID: {e[4]}", 
        "Service": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "Unlock": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "NetworkCleartext": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "NewCredentials": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "RemoteInteractive": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "CachedInteractive": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "CachedRemoteInteractive": lambda e: f"Network Login | Target SID: {e[4]}", 
        # "CachedUnlock": lambda e: f"Network Login | Target SID: {e[4]}" 
    }
    
    def clean_event_data(self, raw_event_datas) -> str:
        elements = [element.text for element in raw_event_datas[0]]
        return f"{logon_types.get(elements[8])} Login completed | Source : {elements[1]}/{elements[2]} (SID : {elements[0]}) | Target : {elements[5]}/{elements[6]} (SID : {elements[4]})", elements