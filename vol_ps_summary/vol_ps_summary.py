# Script pour analyser rapidement le contenu d'un dump Volatility 3 au format csv
# Permet d'analyser rapidement le resultat des modules PsCan et PsList de Volatility3
# -r csv pour obtenir le format csv

# Choix : on ne peut changer que le format du render. Si on veut sauvegarder dans un fichier on utilise la redirection avec ">"
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
    
    return {
        "parameters": config["argparse"]["parameters"].split(",") if "parameters" in config["argparse"] else [],
        "tables_formats": config["argparse"]["tables_formats"].split(",") if "tables_formats" in config["argparse"] else [],
        "output_formats": config["argparse"]["output_formats"].split(",") if "output_formats" in config["argparse"] else [],
        "d_format": config["argparse"].get("d_format", "tab"),
        "d_tablefmt": config["argparse"].get("d_tablefmt", "simple"),
        "d_count": config["argparse"].getboolean("d_count")
    }
    
def parse_arguments(config) :
    parser = argparse.ArgumentParser(description="Quick script to summarize Volatility3 PsList and PsScan output.")
    parser.add_argument("file",         type=str, help="Path to the input CSV file containing the output of PsList or PsScan from Volatility3.")
    parser.add_argument("-p", "--parameters", choices=config["parameters"], default=config["parameters"] , nargs='*', help="List of parameters to extract from the CSV file. If not provided, all available parameters will be used.")
    parser.add_argument("--filter",     type=str, help="A string filter to apply on the data (e.g., 'PPID > 100'). The filter syntax follows pandas' query format. If no filter is provided, all data will be processed.")
    parser.add_argument("-o", "--order",      type=str, help="Specify a column name to order the results by. If not provided, results are shown in the order they appear in the input.")
    parser.add_argument("-r", "--render",      choices=config["output_formats"], default=config["d_format"], help="Specify the format to render the output. Available formats: %(choices)s. Default format is %(default)s.")
    parser.add_argument("-e", "--extract", type=str, default=None, help="extract result in a seperated file")
    parser.add_argument("--inv_order",  action='store_true', help="If set, reverses the order of the results (i.e., descending order). By default, the order is ascending.")
    parser.add_argument("--no_space",   action='store_true', help="If set, removes leading and trailing spaces from the printed output.")
    parser.add_argument("--no_index",   action='store_true', help="If set, omits the index column in the output when rendering tables.")
    parser.add_argument("--tblfmt",     choices=config["tables_formats"], default=config["d_tablefmt"], help="Specify the table format for output when rendering as tabular data. Default format is %(default)s.")
    parser.add_argument("--no_count",   action='store_true', default=not config["d_count"], help="If set, hides the counting feature in the output. Default behavior is to include the count.")
    return parser.parse_args()

def order(df, order, inv_order) :
    if order:
        df.sort_values(by=order, ascending=not inv_order, inplace=True)

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
        "txt": lambda: a.to_string(filename, index=not no_index),
        "csv": lambda: a.to_csv(filename, index=not no_index),
        "json": lambda: a.to_json(filename, index=not no_index),
        "tab": lambda: tabulate(a, headers=headers, tablefmt=tblfmt)
    }

    output = "{}{} {}".format('\n' if not no_space else '', formatters.get(format, lambda: "Invalid format")(), '\n' if not no_space else '')
    if filename and format == "tab":
        write_file(filename, output)
    if not filename:
        print(output)



def parse_data(file) : 
    data = {'name': [], 'time': [], 'ppid': [], 'pid': [], 'subp': []}
    
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile) 
        processes = list(reader) 

    for process in processes :
        process_name = process['ImageFileName']
        if process_name not in data["name"] :
            data["name"].append(process_name)
            data["time"].append(process['CreateTime'])
            data["ppid"].append(int(process['PPID']))
            data["pid"].append(int(process['PID']))
            data["subp"].append(0)
        else : 
            j = data['name'].index(process_name)
            data["subp"][j] += 1
            
    return data

def parse_data(file) : 
    data = {'name': [], 'time': [], 'ppid': [], 'pid': [], 'subp': []}
    
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile) 
        processes = list(reader) 

    for process in processes :
        process_name = process['ImageFileName']
        if process_name not in data["name"] :
            data["name"].append(process_name)
            data["time"].append(process['CreateTime'])
            data["ppid"].append(int(process['PPID']))
            data["pid"].append(int(process['PID']))
            data["subp"].append(0)
        else : 
            j = data['name'].index(process_name)
            data["subp"][j] += 1
            
    return data
    
def analyse(config, args) :
    display_name_mapping = {"name":"Name", "time":"Time", "ppid":"PPID", "pid":"PID", "subp":"Subprocesses"}
    
    data = parse_data(args.file)
    df = pd.DataFrame(data) 
    total = len(df)
    filter(df, args.filter)
    order(df, args.order, args.inv_order)
    count = len(df)
    
    a = df[args.parameters]
    headers = [display_name_mapping[x] for x in a.columns.tolist()]
    render(a, args.extract, args.render, args.no_space, headers, args.tblfmt, args.no_index)
    
    if not args.no_count : 
        print(f"Count: {count}" + f"\nTotal: {total}\n" )

def main() :
    CONFIG_FP = "config.ini"
    config = read_config(CONFIG_FP)
    args = parse_arguments(config)
    analyse(config, args)

if __name__ == "__main__" : 
    main()