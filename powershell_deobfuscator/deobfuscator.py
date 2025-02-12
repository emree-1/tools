import re

def first_clean(input):
    """Prepare all lines before further analysis."""
    res = []
    
    lines = input.split("\n")
    for line in lines : 
        y = line.strip().lower().split(";")
        x = [z.strip() for z in y]
        res += x
    return res

def clean_variables(line):
    def clean(match):
        return match.group().replace("`","")
    
    variable_pattern = r"""\${[\w:`]+}"""
    string_pattern = r"""(["'][\w`]*['"])"""
    
    clean_line = re.sub(variable_pattern, clean, line)
    clean_line = re.sub(string_pattern, clean, clean_line)
    return clean_line
    
    
def final_clean(line):
    # TO DO
    multiple_spaces_pattern = r"""([\s]*)"""

def deobfuscate_format(line):
    pattern_find = r"""[\(]?(["']+[{}0-9]*["'])+\s*-f\s*(["'][\w.\[\]\/:-]+["'](?:\s*,\s*["'][\w.\[\]\/:-]+["'])*)[\)]?"""
    recursion_pattern = r"""[\(]?(['"]*[{}0-9]*['\"])\s*-f\s*(['\"][\w.\[\]\/:-]+['\"](?:\s*,\s*['\"][\w.\[\]:-]+['\"])*),*\s*[\(]*\s*(['\"][{}0-9]*['\"])\s*-f\s*(['\"][\w.\[\]\/:-]+['\"](?:\s*,\s*['\"][\w.\[\]\/:-]+['"])*\s*)[\)]?"""
    previous_str = ""
    current_str = line
    
    while current_str != previous_str:
        previous_str = current_str
        
        matches = re.finditer(pattern_find, current_str)
        if matches : 
            for match in matches : 
                format_string = match.group(1)
                arguments = [re.sub(r"['\"]", "", arg.strip()) for arg in match.group(2).split(",")]
                
                try:
                    res = format_string.format(*arguments)  
                    current_str = current_str.replace(match.group(), res)
                except IndexError:
                    recursion_matches = re.search(recursion_pattern, current_str[match.start():])
                    if recursion_matches :
                        subresult = re.search(pattern_find, current_str[match.end():])
                        if subresult : 
                            try : 
                                format_string = subresult.group(1)
                                arguments = [re.sub(r"['\"]", "", arg.strip()) for arg in match.group(2).split(",")]
                                res = format_string.format(*arguments)  
                                current_str = current_str.replace(subresult.group(),res)
                            except : 
                                pass
    return current_str

def concatenate_strings(line):
    def clean(match):
        res = match.group().replace("'","").replace('"','').replace("+","")
        return f"\"{res}\""
    
    concatenation_pattern = r"""["']([\w:.\/\s]*)["']\s*\+\s*["']([\w:.\/\s]*)["']"""
    previous_str = ""

    current_str = line
    
    while current_str != previous_str:
        previous_str = current_str
        current_str = re.sub(concatenation_pattern, clean, current_str)
    return current_str


with open("tests/big.txt", "r") as f:
    obfuscated = f.read()

lines = first_clean(obfuscated)
cleaned = []
for line in lines : 
    clean_line = deobfuscate_format(line)
    clean_line = clean_variables(clean_line)
    clean_line = concatenate_strings(clean_line)
    cleaned.append(clean_line)
    print(clean_line)
