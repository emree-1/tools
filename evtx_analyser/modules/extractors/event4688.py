from core.EventModule import EventModule

class Event4688Module(EventModule):
    @property
    def name(self) -> str: return "Event ID 4688"
    @property
    def eventID(self) -> str: return "4688"
    @property
    def group(self) -> str: return "process_execution"
    @property
    def xpaths(self) -> list[str] : return [
            "e:EventData/e:Data"
        ]
    
    def clean_event_data(self, raw_event_datas) -> str:
        x = [element.text for element in raw_event_datas[0]]
        # Maybe too verbose, change it to an optional argument
        # return f"""Process created "{x[5].strip()}"  (ID : {x[4]}) | Parent Process: "{x[13]}" | Subject User : {x[1]} (SID : {x[0]}) | Target User : {x[10]} (SID : {x[9]}) | Command Line : {x[8] if not "None" else "-"}"""
        return f"""Process created "{x[5].strip()}" (ID : {x[4]}) | Parent Process: "{x[13]}" """