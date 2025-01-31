# Extract base64 based on provided start

import re
import base64
import pandas as pd
import argparse

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file", type=str, help="File path of the file for keyword search.")
    parser.add_argument("prefix", type=str, help="Prefix in base64.")
    args = parser.parse_args()
    return args


def find_base64_in_file(file_path, prefix):
    base64_pattern = re.compile(r'[A-Za-z0-9+/=]{4,}[^ \n]*')
    results = []
    
    with open(file_path, 'r') as file:
        for line in file:
            for match in base64_pattern.finditer(line):
                base64_str = match.group(0)
                
                if base64_str.startswith(prefix):
                    try:
                        base64.b64decode(base64_str, validate=True)
                        results.append(base64_str)
                    except (base64.binascii.Error, ValueError):
                        continue
    return results

def check_ctf_flag(results) :
    for res in results : 
        if res[-1] == "}" :
            print(res)
    
def b64_decode(encoded_string):
    try:
        padding = len(encoded_string) % 4
        if padding != 0:
            encoded_string += "=" * (4 - padding)

        decoded_bytes = base64.b64decode(encoded_string, validate=True)
        
        decoded_string = decoded_bytes.decode('utf-8', errors='ignore')
        return decoded_string
    except Exception as e:
        print(f"Error : {encoded_string} - {str(e)}")
        return None


args = parse_arguments()
file_path = args.file
prefix = args.prefix
matches = find_base64_in_file(file_path, prefix)
m = set(matches)
results = []
for x in m :
    results.append(b64_decode(x))
    
check_ctf_flag(results)