# Extract base64 based on provided start

import re
import base64
import pandas as pd
import argparse
from tabulate import tabulate
import warnings

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file", type=str, help="File path of the file for keyword search.")
    parser.add_argument("prefix", type=str, help="Prefix in base64.")
    parser.add_argument("--encode", action='store_true', default=False, help="If defined, prefix will be encoded in base64.")
    parser.add_argument("--decode", action='store_true', default=False, help="If defined, outputs will tried to be decoded .")
    parser.add_argument("--ctf", action='store_true', default=False, help="If defined, will return values only ending with \"}\".")
    parser.add_argument("-r", "--render", type=str, choices=["csv", "json", "txt", "tab"], default="csv", help="Specify the format to render the output. Available formats: %(choices)s. Default format is %(default)s.")
    parser.add_argument("-e", "--extract",  type=str, default=None, help="extract result in a seperated file")
    parser.add_argument("--index",       action='store_true', default=False, help="If defined, add index to output.")
    parser.add_argument("--no_space",       action='store_true', help="Remove spaces at the beginning and at the end of the print.")
    args = parser.parse_args()
    return args

def render_txt(results) :
    for x in results :
        print(x)

def write_file(filename, output) :
    with open(filename, 'w') as file :
        file.write(output)

def render(a, filename, format, no_space, index, header=False):
    formatters = {
        "txt": lambda: a.to_csv(filename, index=False, header=False),
        "csv": lambda: a.to_csv(filename, index=index, header=header),
        "json": lambda: a.to_json(filename, index=index),
        "tab": lambda: tabulate(a, headers=["Result"], tablefmt="github", showindex=False)
    }
    
    output = "{}{} {}".format('\n' if not no_space else '', formatters.get(format, lambda: "Invalid format")(), '\n' if not no_space else '')
    if filename and format == "tab":
        write_file(filename, output)
    if not filename :
        print(output)

def ctf_flags(results):
    return [result for result in results if result.endswith("}")]

def b64_encode(keyword, precision=-2):
    b64 = base64.b64encode(keyword.encode('utf-8')).decode('utf-8')
    return b64.rstrip("=")[:precision]

def b64_decode(encoded_strings):
    for encoded_string in encoded_strings:
        try:
            encoded_string = encoded_string.ljust(len(encoded_string) + (4 - len(encoded_string) % 4) % 4, "=")
            decoded_bytes = base64.b64decode(encoded_string, validate=True)
            yield decoded_bytes.decode('utf-8', errors='ignore')
        except (base64.binascii.Error, ValueError) as e:
            warnings.warn(f"Error decoding: {encoded_string} - {e}")

def find_base64_in_file(file_path, prefix):
    base64_pattern = re.compile(r'\b[A-Za-z0-9+/=]{4,}')

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for match in base64_pattern.finditer(line):
                base64_str = match[0]
                
                if base64_str.startswith(prefix):
                    try:
                        base64.b64decode(base64_str, validate=True)
                        yield base64_str 
                    except (base64.binascii.Error, ValueError):
                        pass

def main() :
    args = parse_arguments()
    prefix = b64_encode(args.prefix) if args.encode else args.prefix
    results = set(find_base64_in_file(args.file, prefix))
    
    if args.decode :
        results = list(b64_decode(results))
    if args.ctf :
        results = ctf_flags(results)
    
    df = pd.DataFrame(results)
    pd.set_option('display.max_colwidth', None)

    render(df, args.extract, args.render, args.no_space, args.index)
    
if __name__ == "__main__" :
    main()