import csv
from Levenshtein import distance
import pandas as pd

def filter_similar_strings(strings, threshold=0.95):
    # Liste pour garder les chaînes filtrées
    filtered = []
    
    for s in strings:
        # Comparer la chaîne avec toutes les chaînes déjà filtrées
        keep = True
        for f in filtered:
            # Calculer la similarité
            lev_distance = distance(s, f)
            max_len = max(len(s), len(f))
            similarity = 1 - lev_distance / max_len  # Ratio de similarité basé sur la distance de Levenshtein
            
            # Si la similarité est supérieure au seuil, ne garder qu'une des deux chaînes
            if similarity > threshold:
                keep = False
                break
        
        if keep:
            filtered.append(s)
    
    return filtered




if __name__ == "__main__" :
    df = pd.read_csv("test.csv")
    strings = df["result"].to_list()
        
    result = filter_similar_strings(strings)
    df = pd.DataFrame(result, columns=["result"])
    
    df.to_csv("out.csv", index=False, encoding="utf-8")
    
    print(len(result))