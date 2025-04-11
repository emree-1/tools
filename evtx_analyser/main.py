from core.module_loader import load_modules
from core.EvtxHandler import EvtxHandler
from tabulate import tabulate

def main() :
    # 1. Read the evtx file and parse it
    evtx_events = EvtxHandler.read_evtx("tests/test_small.evtx")
    parsed_events = EvtxHandler.parse_evtx_event_system_info(evtx_events)
    # print(tabulate(parsed_events, headers="keys"))
    
    # 2. Load the modules
    modules = load_modules()
    for module in modules :
        print(module.name)


if __name__ == "__main__":
    main()
