import subprocess
import pandas as pd
from collections import defaultdict
import argparse
import tabulate


def banner() :
    banner = """
   __ __ ___   ___                     
  / //_// _ ) / _ \\ ___ ____ ___ _ ___ 
 / ,<  / _  |/ // /(_-</ __// _ `// _ \\
/_/|_|/____//____//___/\\__/ \\_,_//_//_/
    """
    print(f'\033[38;2;0;210;0m{banner}\033[0m')

    # print(banner)

def parse_arguments() :
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("file", type=str, help="path to pcap file.")
    parser.add_argument("--not_empty", action='store_true', help="Allow devices that sent none empty reports.")
    parser.add_argument("-r", "--render", type=str, choices=["csv", "json", "txt", "tab"], default="csv", help="Specify the output format. Available formats: %(choices)s. Default is %(default)s.")
    parser.add_argument("-e", "--extract", type=str, default=None, help="Save the results to the specified output file.")
    parser.add_argument("--index", action='store_true', default=False, help="Include an index column in the output (useful for CSV/JSON formats).")
    parser.add_argument("--no_space", action='store_true', help="Remove leading and trailing spaces from the output, useful for cleaner result processing.")
    parser.add_argument("-q","--quiet", action='store_true', default=False, help="Suppress the script's banner during execution.")
    args = parser.parse_args()
    return args


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
    output = "Nothing found." if len(output) == 0 else output
    if filename and format == "tab":
        write_file(filename, output)
    if filename : 
        print(f"\nResults saved in \"{filename}\".\n")
    else :
        print(output)

def get_endpoints(file):
    result = subprocess.run(["tshark", "-r", file, "-q", "-z", f"endpoints,usb"], capture_output=True, text=True)
    lines = result.stdout.splitlines()[4:-1]
    data = [line.split() for line in lines if len(line.split()) >= 6]
    df = pd.DataFrame(data, columns=["address", "packets", "_", "tx_packets", "_", "rx_packets", "_"]).drop(columns=["_", "_"])
    df[["packets", "tx_packets", "rx_packets"]] = df[["packets", "tx_packets", "rx_packets"]].astype(int)
    return df

def check_if_any_keyboard(file, devices, not_empty):
    keyboards = defaultdict(int)
    null_reports = set()

    # Exécuter tshark pour récupérer tous les paquets USB
    cmd_result = subprocess.run(["tshark", "-r", file, "-T", "fields", "-e", "usb.src", "-e", "usb.capdata", "-Y", "usb.data_len == 8"],
                                capture_output=True, text=True)

    # Analyser la sortie ligne par ligne
    for line in cmd_result.stdout.splitlines():
        fields = line.split()  # Séparer les champs
        if len(fields) < 2:
            continue  # Ignorer les lignes incomplètes

        device_id, capdata = fields[0], fields[1]

        # Vérifier que la donnée est bien de longueur 8 et que usb.capdata[1] == 00
        if capdata and len(capdata) == 16 and capdata[2:4] == "00":
            keyboards[device_id] += 1  # Compter les paquets valides

        valid_keyboards = [
            d for d in keyboards
            if keyboards[d] == devices.get(d, [0, 0])[1] 
        ]

        if not not_empty and capdata == "0000000000000000" :
            null_reports.add(device_id)
            valid_keyboards = [
                d for d in valid_keyboards
                if d in null_reports
            ]
    
    return {"result" : valid_keyboards}


def main() : 
    args = parse_arguments()

    if not args.quiet : 
        banner()

    endpoints = get_endpoints(args.file)
    T_endpoints = endpoints.set_index("address").T.reset_index(drop=True)
    keyboards = check_if_any_keyboard(args.file, T_endpoints, args.not_empty)
    df = pd.DataFrame(keyboards)

    render(df, args.extract, args.render, args.no_space, args.index)
    

if __name__ == "__main__" : 
    main()