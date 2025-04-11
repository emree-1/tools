from core.EventModule import EventModule

class Event1033Module(EventModule):
    @property
    def name(self) -> str:
        return "Event ID 1033"
    
    @property
    def group(self) -> str:
        return "msi_install"
    
    def parse(self, evtx_event) :
        pass
    
    def match(self, evtx_event):
        return evtx_event['EventID'] == 1033

    def analyze(self, evtx_event):
        return {
            "type": "installation",
            "app": evtx_event.get("ApplicationName", "unknown"),
            "timestamp": evtx_event["TimeCreated"]
        }