# Script pour analyser rapidement le contenu d'un dump Volatility 3 au format csv
# Permet d'analyser rapidement le resultat des modules PsCan et PsList de Volatility3

# Usage : python3 main.py <FILE> <Options>
# Default config can be editted from config.ini

import pandas as pd
import csv
import configparser
import argparse
from tabulate import tabulate

def read_config(config_fp) :
    config = configparser.ConfigParser()
    config.read(config_fp)
    return config

def parse_arguments(config) :
    parameters = config["parameters"].split(",")
    tables_formats = config["tables_formats"].split(",")
    output_formats = config["output_formats"].split(",") 
    d_format  = config["d_format"]
    d_tablefmt = config["d_tablefmt"]
    d_count = config.getboolean("d_count")
    parser = argparse.ArgumentParser(description="Quick script to analyse volatility pslist output.")
    parser.add_argument("file",         type=str, help="File path of the output of pslist with volatility.")
    parser.add_argument("--parameters", choices=parameters, default=parameters , nargs='*', help="Parameter to extract")
    parser.add_argument("--filter",     type=str, help="Filter.")
    parser.add_argument("--order",      type=str, help="order result.")
    parser.add_argument("--format",     choices=output_formats, default=d_format, help="Filter.")
    parser.add_argument("--tblfmt",     choices=tables_formats, default=d_tablefmt, help="Format de la table.")
    parser.add_argument("--inv_order",  action='store_true', help="Inverse order of ordering.")
    parser.add_argument("--no_space",   action='store_true', help="Remove spaces at the beginning and at the end of the print.")
    parser.add_argument("--no_count",   action='store_true', default=not d_count, help="Format de la table.")
    args = parser.parse_args()
    return args

def analyse(config, args) :
    display_name_mapping = {"name":"Name", "time":"Time", "ppid":"PPID", "pid":"PID", "subp":"Subprocesses"}
    data = {'name': [], 'time': [], 'ppid': [], 'pid': [], 'subp': []}
    i = 0
    
    with open(args.file, 'r') as csvfile:
        reader = csv.DictReader(csvfile) 
        processes_raw = list(reader) 
        
    for process in processes_raw :
        process_name = process['ImageFileName']
        if process_name not in data["name"] :
            data["name"].append(process_name)
            data["time"].append(process['CreateTime'])
            data["ppid"].append(int(process['PPID']))
            data["pid"].append(int(process['PID']))
            data["subp"].append(0)
            i += 1
        else : 
            j = data['name'].index(process_name)
            data["subp"][j] += 1
    
    df = pd.DataFrame(data) 
    total = len(df)
    
    # Filter
    if args.filter : 
        filter = args.filter.lower()
        if " in " in filter:
            value, column = filter.split(" in ")
            column = column.strip()
            value = value.strip("'\"")
            df = df[df[column].str.contains(value, case=False, na=False)]
        else : 
            df = df.query(filter)
    count = len(df)
    
    # Order
    ascending = not args.inv_order
    if args.order : 
        df = df.sort_values(by=args.order, ascending=ascending)
    
    a = df[args.parameters]
    headers = [display_name_mapping[x] for x in a.columns.tolist()]
    
    # Format
    if args.format == "list" :
        pass
        if type(a) is pd.Series :
            print(a.to_list())
        elif type(a) is pd.DataFrame : 
            print(a.values.tolist())
    elif args.format == "csv" : 
        print(a.to_csv())
    elif args.format == "ocsv" : 
        pass
    elif args.format == "json" : 
        print(a.to_json())
    elif args.format == "tab" : 
        if args.no_space : 
            print(tabulate(a, headers=headers, tablefmt=args.tblfmt))
        else : 
            print("\n" + tabulate(a, headers=headers, tablefmt=args.tblfmt) + "\n")
            
    # Count
    if not args.no_count : 
        print(f"\nCount: {count}" + f"\nTotal: {total}\n" )

def main() :
    CONFIG_FP = "config.ini"
    config = read_config(CONFIG_FP)
    args = parse_arguments(config["argparse"])
    analyse(config, args)

if __name__ == "__main__" : 
    main()