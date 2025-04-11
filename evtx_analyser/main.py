from core.EvtxHandler import EvtxHandler
from tabulate import tabulate

def main() :
    evtx_events = EvtxHandler("tests/test_msi_install.evtx").read_and_parse_evtx()
    
    print(tabulate(evtx_events, headers="keys"), "\n ")

if __name__ == "__main__":
    main()
