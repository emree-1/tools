# Keeps longest version of a string
# if a string is included intot an other one, it will keep the longest one
# ex :  "abc" and "abcde" will keep "abcde"

import pandas as pd


def main(strings ) :
    strings.sort(key=len, reverse=True)
    
    filtered_set = set()
    filtered = []
    
    for s2 in strings:
        s = s2.lower()
        if not any(s in other for other in filtered_set):
            filtered.append(s2)
            filtered_set.add(s)
    
    return filtered

if __name__ == "__main__" :
    df = pd.read_csv("test.csv")
    strings = df["result"].to_list()
    result = main(strings)
    df = pd.DataFrame(result)
    df.to_csv("out.csv", index=False, encoding="utf-8")
