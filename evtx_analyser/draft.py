import html
import argparse
import re

from Evtx.Evtx import Evtx
from enum import Enum
import xml.etree.ElementTree as ET
from tabulate import tabulate


# TO DO : test on a dataset that includes event ID 11708

ns = {'e': 'http://schemas.microsoft.com/win/2004/08/events/event'}

class event_ids(Enum):
    msi_installer_install_event_ids = ['1033', '11707', '11708'] # Principaux Event IDs MSI


language_mapping = {
    "1033" : "English - United States"
}

exit_status = { 
    "0" : "Downloaded successfuly"
}


def parse_arguments() :
    parser = argparse.ArgumentParser(description="Collect and displays events related to downloads with Windos Installer from evtx file.")
    parser.add_argument("file", type=str, help="File path of the evtx file.")
    parser.add_argument("--verbose",        action='store_true', help="verbose mode.")
    args = parser.parse_args()
    return args



def extract_evtx_from_file_as_xml(evtx_file) :
    try : 
        with Evtx(evtx_file) as log:
            return [record.xml() for record in log.records()]
    except :
        print("Error when trying to read the evtx file.")

def parse_evtx_list(evtx_events):
    tab = {"TimeCreated":[], "EventRecordID":[], "EventID":[], "Provider":[], "Channel":[], "Computer":[], "Data":[]}
    
    for evtx_event in evtx_events :
        root = ET.fromstring(evtx_event)
        
        event_id = root.find('./e:System/e:EventID', ns).text if not None else None
        if event_id not in event_ids.msi_installer_install_event_ids.value :
            continue

        tab["TimeCreated"].append(root.find('./e:System/e:TimeCreated', ns).attrib.get("SystemTime") if not None else None)
        tab["EventRecordID"].append(root.find('./e:System/e:EventRecordID', ns).text if not None else None)
        tab["EventID"].append(event_id)
        tab["Provider"].append(root.find('./e:System/e:Provider', ns).attrib.get("Name") if not None else None)
        tab["Channel"].append(root.find('./e:System/e:Channel', ns).text if not None else None)
        tab["Computer"].append(root.find('./e:System/e:Computer', ns).text if not None else None)
        tab["Data"].append(clean_data(root.find('./e:EventData/e:Data', ns).text if not None else None, event_id))

    return tab

def clean_data(data, event_id):
    cleaned_data = html.unescape(data)
    cleaned_data = re.sub(r'<string>\(NULL\)</string>', '', cleaned_data) 
    cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()
    pattern = r'<string>(.*?)<\/string>'
    cleaned_data = re.sub(r'<string></string>', '', cleaned_data)  
    x = re.findall(pattern, cleaned_data)
    if event_id == "1033" :
        return f"{x[0]} ({x[1]}) | {x[4]} | {language_mapping.get(x[2])} | {exit_status.get(x[3])}"
    return x[0]

def create_summary(download_events):
    summary_table = {"Time":[], "Program":[]}
    pattern = r" ([a-zA-Z+_0-9 ]*) -"
    
    for i in range(len(download_events["TimeCreated"])) :
        if download_events['EventID'][i] == "11707" : 
            x = re.findall(pattern, download_events['Data'][i])
            if x[0].strip() not in summary_table["Program"] :
                summary_table["Time"].append(download_events['TimeCreated'][i])
                summary_table["Program"].append(x[0].strip())
    return summary_table

def main() :
    args = parse_arguments()
    evtx_event_list = extract_evtx_from_file_as_xml(args.file)
    download_events = parse_evtx_list(evtx_event_list)
    summary_table = create_summary(download_events)
    if args.verbose : 
        print(tabulate(download_events, headers="keys"), "\n ")
    print(" === SUMMARY ===\n\n", tabulate(summary_table, headers="keys"), "\n")
    

if __name__ == "__main__":
    main()
