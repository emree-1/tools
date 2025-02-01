# Keeps longest version of a string
# if a string is included into an other one, it will keep the longest one
# ex :  "abc" and "abcde" will keep "abcde"

import pandas as pd
import argparse
import time

def parse_arguments() :
    parser = argparse.ArgumentParser(description="Quick script to search for keywords in a text file.")
    parser.add_argument("file", type=str, help="File path of the file for keyword search.")
    parser.add_argument("--time", action='store_true', default=False, help="Display execution time.")
    parser.add_argument("--no_summary", action='store_false', default=True, help="If set, hides summary.")
    args = parser.parse_args()
    return args

def read_strings(filename) :
    df = pd.read_csv(filename)
    strings = df["result"].to_list()
    return strings

def keep_longest(strings) :
    strings.sort(key=len, reverse=True)
    filtered_set = set()
    filtered = []
    
    for s2 in strings:
        s = s2.lower()
        if not any(s in other for other in filtered_set):
            filtered.append(s2)
            filtered_set.add(s)
    return filtered

def visualise(results, total, summary) :
    df = pd.DataFrame(results, columns=["result"])
    
    if summary : 
        print(f"\nCount : {len(df['result'])}")
        print(f"Removed : {total - len(df['result'])}")
        print(f"Total : {total}")
        print(df)
    df.to_csv("out.csv", index=False, encoding="utf-8")

def main() :
    start = time.time()
    args = parse_arguments()
    strings = read_strings(args.file)
    results = keep_longest(strings)
    visualise(results, len(strings), args.no_summary)
    end = time.time()
    if args.time :
        print(end - start)

if __name__ == "__main__" :
    main()
    
