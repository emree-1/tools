from core.EvtxHandler import EvtxHandler
from tabulate import tabulate
import argparse

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Collect and displays events related to downloads with Windos Installer from evtx file.")
    parser.add_argument("file", type=str, help="File path of the evtx file.")
    parser.add_argument("--verbose", action='store_true', help="verbose mode.")
    args = parser.parse_args()
    return args

def keyword_search(raw_evtx_events, IoCs):
    for evtx_event in raw_evtx_events :
        print(evtx_event)

def main() :
    args = parse_arguments()
    evtx_handler = EvtxHandler(args.file)
    raw_evtx_events = evtx_handler.read_evtx(args.file)
    
    # for event in raw_evtx_events:
    #     print(event)
    
    evtx_events = evtx_handler.parse_evtx(raw_evtx_events)
    IoCs = ["Totally_Legit_Software", "cGljb0NURntFdjNudF92aTN3djNyXw==", "shutdown.exe"]
    
    # x = [raw_evtx_event for raw_evtx_event in raw_evtx_events if any(ioc in raw_evtx_event for ioc in IoCs)]
    # for y in x :
    #     print(y)
        
    print(tabulate(evtx_events, headers="keys"))
    
    # print("Do not trust Program names and manufacturers as they can easily be manipulated.")
    
    
    
    

if __name__ == "__main__":
    main()
