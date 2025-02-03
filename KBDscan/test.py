import argparse

parser = argparse.ArgumentParser(description="...")
parser.add_argument("file", type=str, help="path to pcap file.")
args = parser.parse_args()

print(args.file)