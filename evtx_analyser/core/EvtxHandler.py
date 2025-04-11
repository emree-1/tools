from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET

from core.ModuleHandler import ModuleHandler

class EvtxHandler:
    def __init__(self, evtx_file):
        self.evtx_file = evtx_file
        self.ns = {'e': 'http://schemas.microsoft.com/win/2004/08/events/event'}
        self.modules = ModuleHandler.load_modules("extractors")
        self.evtx_events = {
            "TimeCreated": [],
            "EventRecordID": [],
            "EventID": [],
            "Provider": [],
            "Channel": [],
            "Computer": [],
            "Data": []
        }
        
    def read_and_parse_evtx(self):
        evtx_events = self.read_evtx(self.evtx_file)
        return self.parse_evtx(evtx_events)
    
    def read_evtx(self, evtx_file):
        try:
            with Evtx(evtx_file) as log:
                return [record.xml() for record in log.records()]
        except Exception as e:
            print(f"Error when trying to read the evtx file: {e}")
            return []
    
    def parse_evtx(self, evtx_events):

        xpaths = {
            "TimeCreated": './e:System/e:TimeCreated',
            "EventRecordID": './e:System/e:EventRecordID',
            "EventID": './e:System/e:EventID',
            "Provider": './e:System/e:Provider',
            "Channel": './e:System/e:Channel',
            "Computer": './e:System/e:Computer'
        }

        for i, evtx_event in enumerate(evtx_events):
            root = ET.fromstring(evtx_event)
            
            # Parse system information
            for key, xpath in xpaths.items():
                element = root.find(xpath, self.ns)
                value = None
                if element is not None:
                    if key == "TimeCreated":
                        value = element.attrib.get("SystemTime")
                    elif key == "Provider":
                        value = element.attrib.get("Name")
                    else:
                        value = element.text
                self.evtx_events[key].append(value)
        
            # Parse event data
            extractor_module = self.modules.get(self.evtx_events["EventID"][i], None)
            if extractor_module is None:
                # Add a logging message here to indicate that no module was found for the event ID
                self.evtx_events["Data"].append("")
                continue
            event_data = extractor_module.parse_event_data(evtx_event)
            self.evtx_events["Data"].append(event_data)
            
        return self.evtx_events

