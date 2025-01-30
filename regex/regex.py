import pandas as pd
import re 
import argparse

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file", type=str, help="File path of the file for keyword search.")
    parser.add_argument("-r", "--regex", type=str, help="Regex.")
    args = parser.parse_args()
    return args


def main():
    # Analyse des arguments
    args = parse_arguments()
    results = {"result":[]}
    # Compilation de l'expression régulière
    pattern = re.compile(args.regex)
    count = 0
    try:
        # Ouverture du fichier et lecture ligne par ligne
        with open('test.txt', "r") as f:
            for i, line in enumerate(f):
                # Recherche de la correspondance dans chaque ligne
                if re.search(pattern, line):
                    # print(f"Match : {i} - {line}", end="")  # Affiche la ligne correspondante
                    print(f"{line}", end="")
                    results["result"].append(re.sub(r'\n', '', line))
                    count += 1
    except FileNotFoundError:
        print("Erreur : Le fichier 'test.txt' est introuvable.")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier : {e}")
    print(f"Total: {count}")
    
    df = pd.DataFrame(results)
    df.to_csv("out.csv", index=False, encoding='utf-8')


if __name__ == "__main__" :
    main()