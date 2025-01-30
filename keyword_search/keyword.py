# Keyword search in a txt file
# Useful to search kword in strings output for example

import base64
import argparse
from tabulate import tabulate
import configparser
import pandas as pd
import time
import re

def read_config(config_fp) :
    config = configparser.ConfigParser()
    config.read(config_fp)
    
    return {
        "parameters": config["argparse"]["parameters"].split(","),
        "order_parameters": config["argparse"]["order_parameters"].split(","),
        "tables_formats": config["argparse"]["tables_formats"].split(","),
        "output_formats": config["argparse"]["output_formats"].split(","),
        "variants": config["argparse"]["variants"].split(","),
        "d_format": config["argparse"]["d_format"],
        "d_tablefmt": config["argparse"]["d_tablefmt"],
        "d_summary": config["argparse"].getboolean("d_summary"),
        "d_hide_zero": config["argparse"].getboolean("d_hide_zero"),
        "d_remove_double": config["argparse"].getboolean("d_remove_double"),
        "d_variants": config["argparse"]["d_variants"].split(","),
        "d_output_format": config["argparse"]["d_output_format"]
    }

def parse_arguments(config) :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file",             type=str, help="File path of the file for keyword search.")
    parser.add_argument("-k", "--keywords", type=str, default=[], nargs='+', help="Keywords to search for.")
    parser.add_argument("-v", "--variants", type=str, choices=config["variants"], default=config["d_variants"], nargs='*', help="Variants to generate.")
    parser.add_argument("-s", "--summary",  action='store_true', default=config["d_summary"], help="Display a summary table.")
    parser.add_argument("--min",            type=int, help="minimum count.")
    parser.add_argument("--max",            type=int, help="maximum count.")
    parser.add_argument("--no_plain",       action='store_true', help="remove plain user keywords.")
    parser.add_argument("--hide_zero",      action='store_true', default=config["d_hide_zero"], help="Filter.")
    parser.add_argument("--parameters", choices=config["parameters"], default=config["parameters"] , nargs='*', help="List of parameters to extract from the CSV file. If not provided, all available parameters will be used.")
    parser.add_argument("--verbose",        action='store_true', default=False, help="verbose mode.")
    parser.add_argument("-e", "--extract", type=str, default=None, help="extract result in a seperated file")
    parser.add_argument("-r", "--render",      choices=config["output_formats"], default=config["d_format"], help="Specify the format to render the output. Available formats: %(choices)s. Default format is %(default)s.")
    parser.add_argument("--order",          type=str, choices=config["order_parameters"],  help="order result.")
    parser.add_argument("--tblfmt",         type=str, choices=config["tables_formats"], default=config["d_tablefmt"], help="Format de la table.")
    parser.add_argument("--inv_order",      action='store_true', help="Inverse order of ordering.")
    parser.add_argument("--remove_double",  action='store_true', default=config["d_remove_double"], help="remove double matches.")
    parser.add_argument("--cesar_shift",    type=int, default=None, nargs='*', help="shifts to perform.")
    parser.add_argument("--outfile",        type=str, default=None, help="output filte to save in.")
    parser.add_argument("--no_index",       action='store_true', default=False, help="Display/extract with index.")
    parser.add_argument("--time",       action='store_true', default=False, help="Display execution time.")
    parser.add_argument("--case_sensitive",       type=str, default="utf-8", help="make the search case sensitive.")
    parser.add_argument("--no_space",       action='store_true', help="Remove spaces at the beginning and at the end of the print.")
    args = parser.parse_args()
    return args

def filter(df, filter_str):
    if filter_str:
        filter_str = filter_str.lower()
        if " in " in filter_str:
            value, column = filter_str.split(" in ")
            column = column.strip()
            value = value.strip("'\"")
            df.drop(df[~df[column].str.contains(value, case=False, na=False)].index, inplace=True)
        else:
            df.query(filter_str, inplace=True)

def write_file(filename, output) :
    with open(filename, 'w') as file :
        file.write(output)

def render(a, filename, format, no_space, headers, tblfmt, no_index, ):
    formatters = {
        "txt": lambda: a.to_string(filename, index= not no_index),
        "csv": lambda: a.to_csv(filename, index= not no_index),
        "json": lambda: a.to_json(filename, index= not no_index),
        "tab": lambda: tabulate(a, headers=headers, tablefmt=tblfmt, showindex=False)
    }

    output = "{}{} {}".format('\n' if not no_space else '', formatters.get(format, lambda: "Invalid format")(), '\n' if not no_space else '')
    if filename and format == "tab":
        write_file(filename, output)
    if not filename:
        print(output)

def add_keywords(user_keywords, keywords, source, encoding_func, options):
    for keyword in user_keywords:
        encoded_keyword, encode_source = encoding_func(keyword, source, options)
        keywords["keyword"].append(encoded_keyword)
        keywords["source"].append(encode_source)
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

def cesar_cipher(keyword, source, options):
    shift = options["shift"]
    result = ""
    for char in keyword:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result, f"{source} ({keyword})"

def cesar_gen(user_keywords, keywords, source, shifts) :
    for shift in shifts:
        add_keywords(user_keywords, keywords, f"cesar - {shift}", cesar_cipher, {"shift":shift})

def parse_data(file, keywords, options):
    results = {'line_num':[], 'keyword':[], 'result':[]}
    seen_lines = set()  # Utiliser un set pour vérifier les doublons rapidement
    keywords_lower = [kw.lower() for kw in keywords["keyword"]]  # Pré-convertir les mots-clés en minuscule
    
    with open(file, 'r') as file:
        for j, line in enumerate(file):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()  # Convertir la ligne une seule fois
            for i, keyword in enumerate(keywords_lower):
                if keyword in line_lower:
                    if options["remove_double"] and line_stripped not in seen_lines:
                        seen_lines.add(line_stripped)
                        results["line_num"].append(j)
                        results["result"].append(line_stripped)
                        results["keyword"].append(keywords["keyword"][i])
                        keywords["count"][i] += 1
                    elif not options["remove_double"]:
                        results["line_num"].append(j)
                        results["result"].append(line_stripped)
                        results["keyword"].append(keywords["keyword"][i])
                        keywords["count"][i] += 1
                    
                    if options["verbose"]:
                        print(f"{j} | {keywords['keyword'][i]} | {line_stripped}")
    
    return results

def generate_keywords(user_keywords, variants, options) :
    keywords = {'keyword': [], 'source': [], 'count': []}
    
    generators = {
        "user": lambda: add_keywords(user_keywords, keywords, "user", no_encode, options),
        "hex": lambda: add_keywords(user_keywords, keywords, "hex", hex_encode, options),
        "b64": lambda: add_keywords(user_keywords, keywords, "b64", b64_encode, options),
        "cesar": lambda: cesar_gen(user_keywords, keywords, "cesar", options["cesar_shift"])
    }
    
    for variant in variants:
        generators[variant]()
        
    print(f"\n  > KEYWORDS \n\n {' || '.join(keywords['keyword'])}")
        
    return keywords

def visualise(keywords, results, args):
    df = pd.DataFrame(keywords)

    filter_conditions = []
    if args.hide_zero:
        filter_conditions.append("count > 0")
    if args.min:
        filter_conditions.append(f"count > {args.min}")
    if args.max:
        filter_conditions.append(f"count < {args.max}")
    if filter_conditions:
        df = df.query(" and ".join(filter_conditions))
    
    if args.order:
        df = df.sort_values(by=args.order, ascending=not args.inv_order)

    if args.summary:
        print(f"\n  > SUMMARY \n\n{tabulate(df, headers='keys', tablefmt=args.tblfmt)}\n")

    df_results = pd.DataFrame(results)
    print(f"Total : {len(results['result'])}\n")
    render(df_results[args.parameters], args.extract, args.render, args.no_space, df_results.columns.tolist(), args.tblfmt, args.no_index)

def set_options(args) : 
    options = {}
    options["cesar_shift"] = args.cesar_shift if args.cesar_shift else range(1,26)
    options["remove_double"] = args.remove_double 
    options["trim_padding"] = True
    options["verbose"] = args.verbose 
    return options

def main() :
    start = time.time()
    CONFIG_FP = "config.ini"
    config = read_config(CONFIG_FP)
    args = parse_arguments(config)
    options = set_options(args)
    keywords = generate_keywords(args.keywords, args.variants, options)
    results = parse_data(args.file, keywords, options)
    visualise(keywords, results, args)
    end = time.time()
    if args.time :
        print(end - start)
    
if __name__ == "__main__" :
    main()