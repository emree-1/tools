from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET

ns = {'e': 'http://schemas.microsoft.com/win/2004/08/events/event'}

class EvtxHandler:
    @staticmethod
    def read_evtx(evtx_file):
        try:
            with Evtx(evtx_file) as log:
                return [record.xml() for record in log.records()]
        except Exception as e:
            print(f"Error when trying to read the evtx file: {e}")
            return []
    
    @staticmethod
    def parse_evtx_event_system_info(evtx_events):
        parsed_events = {
            "Index": [],
            "TimeCreated": [],
            "EventRecordID": [],
            "EventID": [],
            "Provider": [],
            "Channel": [],
            "Computer": []
        }

        xpaths = {
            "TimeCreated": './e:System/e:TimeCreated',
            "EventRecordID": './e:System/e:EventRecordID',
            "EventID": './e:System/e:EventID',
            "Provider": './e:System/e:Provider',
            "Channel": './e:System/e:Channel',
            "Computer": './e:System/e:Computer'
        }

        append = parsed_events["Index"].append  # Cache method for performance
        for i, evtx_event in enumerate(evtx_events):
            root = ET.fromstring(evtx_event)
            append(i)  # Append index
            for key, xpath in xpaths.items():
                element = root.find(xpath, ns)
                value = None
                if element is not None:
                    if key == "TimeCreated":
                        value = element.attrib.get("SystemTime")
                    elif key == "Provider":
                        value = element.attrib.get("Name")
                    else:
                        value = element.text
                parsed_events[key].append(value)

        return parsed_events


