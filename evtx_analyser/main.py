from core.EvtxHandler import EvtxHandler
from tabulate import tabulate
import argparse

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Collect and displays events related to downloads with Windos Installer from evtx file.")
    parser.add_argument("file", type=str, help="File path of the evtx file.")
    parser.add_argument("--verbose", action='store_true', help="verbose mode.")
    args = parser.parse_args()
    return args

def main() :
    args = parse_arguments()
    evtx_events = EvtxHandler(args.file).read_and_parse_evtx()

    print(tabulate(evtx_events, headers="keys"), "\n ")

if __name__ == "__main__":
    main()
