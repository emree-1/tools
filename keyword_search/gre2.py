# Keyword search in a txt file

import base64
import argparse
from tabulate import tabulate
import configparser
import pandas as pd
import re

def read_config(config_fp) :
    config = configparser.ConfigParser()
    config.read(config_fp)
    return config

def add_keywords(user_keywords, keywords, source, encoding_func, trim_padding=False):
    for keyword in user_keywords:
        encoded_keyword, encde_source = encoding_func(keyword, source, trim_padding)
        keywords["keyword"].append(encoded_keyword)
        keywords["source"].append(encde_source)
        keywords["count"].append(0)

def no_encode(keyword, source, options=None) :
    return keyword, source

def hex_encode(keyword, source, options=None):
    return str(keyword.encode('utf-8').hex()), f"{source} ({keyword})"

def b64_encode(keyword, source, options=None):
    b64 = base64.b64encode(keyword.encode('utf-8')).decode('utf-8')
    if options.get("trim_padding", None):
        return b64.rstrip("=")[:-2], f"{source} ({keyword})"  # Enlever le padding et ajuster la précision si nécessaire
    return b64, f"{source} ({keyword})"

def cesar_cipher(keyword, source, options=None):
    result = ""
    shift = options.get("shift",None)
    for char in keyword:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result, f"{source} ({keyword})"

def extract(df, outformat, outfile, options=None) :
    # Si on specifie un outfile le resultat est extrait

    if outformat == "list" :
        if type(df) is pd.Series :
            out = df.to_list()
        elif type(df) is pd.DataFrame : 
            out = df.values.tolist() 
    elif outformat == "csv" : 
        out = df.to_csv(outfile, index=not options["index"], encoding=options["encoding"])
    elif outformat == "json" : 
        out = df.to_json(outfile, index=not options["index"])
    elif outformat == "tab" : 
        out = f"{'' if options.get('no_space',False) else chr(10)}{tabulate(df, headers='keys', tablefmt='github')}{'' if options.get('no_space',False) else chr(10)}"
        if not outfile : 
            print(out)
        else : 
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(out)
        
def parse_arguments(config) :
    parameters = config["parameters"].split(",")
    tables_formats = config["tables_formats"].split(",")
    output_formats = config["output_formats"].split(",") 
    d_output_format = config["d_output_format"]
    d_tablefmt = config["d_tablefmt"]
    variants = config["variants"].split(",")
    d_variants = config["d_variants"].split(",")
    d_summary = config.getboolean("d_summary")
    d_hide_zero = config.getboolean("d_hide_zero")
    d_remove_double = config.getboolean("d_remove_double")
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file",             type=str, help="File path of the file for keyword search.")
    parser.add_argument("-k", "--keywords", type=str, nargs='+', help="Keywords to search for.")
    parser.add_argument("-v", "--variants", type=str, choices=variants, default = d_variants, nargs='*', help="Variants to generate.")
    parser.add_argument("-s", "--summary",  action='store_true', default=d_summary, help="Display a summary table.")
    parser.add_argument("--min",            type=int, help="minimum count.")
    parser.add_argument("--max",            type=int, help="maximum count.")
    parser.add_argument("--no_plain",       action='store_true', help="remove plain user keywords.")
    parser.add_argument("--hide_zero",      action='store_true', default=d_hide_zero, help="Filter.")
    parser.add_argument("--verbose",        action='store_true', default=False, help="verbose mode.")
    parser.add_argument("--outformat", choices=output_formats, default=d_output_format, help="extract format.")
    parser.add_argument("--order",          type=str, choices=parameters,  help="order result.")
    parser.add_argument("--tblfm",         type=str, choices=tables_formats, default=d_tablefmt, help="Format de la table.")
    parser.add_argument("--inv_order",      action='store_true', help="Inverse order of ordering.")
    parser.add_argument("--remove_double",  action='store_true', default=d_remove_double, help="remove double matches.")
    parser.add_argument("--cesar_shift",    type=int, default=None, nargs='*', help="shifts to perform.")
    parser.add_argument("--outfile",        type=str, default=None, help="output filte to save in.")
    parser.add_argument("--no_index",       action='store_true', default=False, help="Display/extract with index.")
    parser.add_argument("--encoding",       type=str, default="utf-8", help="Display/extract index.")
    parser.add_argument("--case_sensitive",       type=str, default="utf-8", help="make the search case sensitive.")
    parser.add_argument("--no_space",       action='store_true', help="Remove spaces at the beginning and at the end of the print.")
    args = parser.parse_args()
    return args

def analyse(args) :
    user_keywords = args.keywords
    keywords = {'keyword': [], 'source': [], 'count': []}
    results = {'line_num':[], 'keyword':[], 'result':[]}
    options = {}
    
    if not args.no_plain : 
        add_keywords(user_keywords, keywords, "user", no_encode)
    if "hex" in args.variants : 
        add_keywords(user_keywords, keywords, "hex", hex_encode)
    if "b64" in args.variants : 
        options["trim_padding"] = True
        add_keywords(user_keywords, keywords, "b64", b64_encode, options)
    if "cesar" in args.variants :     
        shifts = args.cesar_shift if args.cesar_shift else range(1, 26)
        for shift in shifts:
            options["shift"] = shift
            add_keywords(user_keywords, keywords, f"cesar - {shift}", cesar_cipher, options)
        
    print(f"\n  > KEYWORDS \n\n {' || '.join(keywords['keyword'])}")
    
    pattern = re.compile('(' + '|'.join(map(re.escape, keywords['keyword'])) + ')', re.IGNORECASE)

    with open(args.file, 'r') as file:
        j = 0
        for line in file:
            matches = pattern.findall(line)
            if matches : 
                print(matches)
                
    print(keywords["keyword"])
    #         for i, keyword in enumerate(keywords["keyword"]) :
    #             if keyword.lower() in line.lower():
    #                 if args.remove_double and line.strip() not in results["result"] :
    #                     results["line_num"].append(j)
    #                     results["result"].append(line.strip())
    #                     results["keyword"].append(keyword)
    #                     keywords["count"][i] += 1
    #                 elif not args.remove_double: 
    #                     results["line_num"].append(j)
    #                     results["result"].append(line.strip())
    #                     results["keyword"].append(keyword)
    #                     keywords["count"][i] += 1
                    
    #                 if args.verbose : 
    #                     print(f"{j} | {keyword} | {line.strip()}")
    #         j += 1

    # df = pd.DataFrame(keywords)
    
    # if args.hide_zero :
    #     df = df[df["count"] > 0]
        
    # if args.min : 
    #     df = df[df["count"] > args.min]
        
    # if args.max : 
    #     df = df[df["count"] < args.max]
        
    # ascending = not args.inv_order
    # if args.order : 
    #     df = df.sort_values(by=args.order, ascending=ascending)

    # if args.summary : 
    #     print("\n  > SUMMARY \n\n" + tabulate(df, headers='keys', tablefmt=args.tblfm) + "\n")
    
    # df = pd.DataFrame(results)  
    
    # print(f"Total : {len(results['result'])}\n")
    
    # options["index"] = args.no_index
    # options["encoding"] = args.encoding
    # options["no_space"] = args.no_space
    # extract(df, args.outformat, args.outfile, options)

def main() :
    CONFIG_FP = "config.ini"
    config = read_config(CONFIG_FP)
    args = parse_arguments(config["argparse"])
    analyse(args)

if __name__ == "__main__" : 
    main()