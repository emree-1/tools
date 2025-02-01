# Extract base64 based on provided start

import re
import base64
import pandas as pd
import argparse
import tabulate

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file", type=str, help="File path of the file for keyword search.")
    parser.add_argument("prefix", type=str, help="Prefix in base64.")
    parser.add_argument("--encode", action='store_true', default=False, help="If defined, prefix will be encoded in base64.")
    parser.add_argument("--decode", action='store_true', default=False, help="If defined, outputs will tried to be decoded .")
    parser.add_argument("--ctf", action='store_true', default=False, help="If defined, will return values only ending with \"}\".")
    parser.add_argument("-r", "--render", type=str, choices=["csv", "json", "txt", "tab"], default="csv", help="Specify the format to render the output. Available formats: %(choices)s. Default format is %(default)s.")
    parser.add_argument("--outfile", type=str, default=None, help="output filte to save in.")
    parser.add_argument("-e", "--extract",  type=str, default=None, help="extract result in a seperated file")
    parser.add_argument("--tblfmt",         type=str, choices="github", default="github", help="Format de la table.")
    parser.add_argument("--index",       action='store_true', default=False, help="If defined, add index to output.")
    parser.add_argument("--quiet",      action='store_true', help="Don't print output.")
    parser.add_argument("--no_space",       action='store_true', help="Remove spaces at the beginning and at the end of the print.")
    args = parser.parse_args()
    return args

def render_txt(results) :
    for x in results :
        print(x)

def write_file(filename, output) :
    with open(filename, 'w') as file :
        file.write(output)

def render(a, filename, format, no_space, headers, tblfmt, index, quiet, header=False):
    formatters = {
        "txt": lambda: a.to_string(filename, index= index, header=header),
        "csv": lambda: a.to_csv(filename, index=index, header=header),
        "json": lambda: a.to_json(filename, index=index),
        "tab": lambda: tabulate(a, headers=headers, tablefmt=tblfmt, showindex=False)
    }
    
    output = "{}{} {}".format('\n' if not no_space else '', formatters.get(format, lambda: "Invalid format")(), '\n' if not no_space else '')
    if filename and format == "tab":
        write_file(filename, output)
    if not filename and not quiet:
        print(output)

def ctf_flags(results) :
    flags = []
    for result in results : 
        if result[-1] == "}" :
            flags.append(result)
    return flags    

def b64_encode(keyword, precision=-2):
    b64 = base64.b64encode(keyword.encode('utf-8')).decode('utf-8')
    return b64.rstrip("=")[:precision]

def b64_decode(encoded_strings):
    decoded = []
    for encoded_string in encoded_strings :
        try:
            padding = len(encoded_string) % 4
            if padding != 0:
                encoded_string += "=" * (4 - padding)

            decoded_bytes = base64.b64decode(encoded_string, validate=True)
            
            decoded_string = decoded_bytes.decode('utf-8', errors='ignore')
            decoded.append(decoded_string)
        except Exception as e:
            print(f"Error : {encoded_string} - {str(e)}")
            return None
    return decoded

def find_base64_in_file(file_path, prefix):
    base64_pattern = re.compile(r'[A-Za-z0-9+/=]{4,}')
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

def main() :
    args = parse_arguments()
    prefix = b64_encode(args.prefix) if args.encode else args.prefix
    results = set(find_base64_in_file(args.file, prefix))

    if args.decode :
        results = b64_decode(results)
    if args.ctf : 
        results = ctf_flags(results)
        
    df = pd.DataFrame(results, columns=["result"])
    render(df, args.extract, args.render, args.no_space, None, args.tblfmt, args.index, args.quiet)
    
if __name__ == "__main__" :
    main()