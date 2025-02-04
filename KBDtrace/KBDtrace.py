
# Original code is from  : https://github.com/TeamRocketIst/ctf-usb-keyboard-parser/blob/master/usbkeyboard.py
# Just used tshark with subprocess to automate extraction

import argparse
import subprocess
import pandas as pd

def banner(quiet) :
    if quiet : 
        return
    banner = """
   __ _____  ___  __                  
  / //_/ _ )/ _ \\/ /________ ________ 
 / ,< / _  / // / __/ __/ _ `/ __/ -_)
/_/|_/____/____/\\__/_/  \\_,_/\\__/\\__/                               
"""
    print(banner)


KEY_CODES = {
    0x04:['a', 'A'],
    0x05:['b', 'B'],
    0x06:['c', 'C'],
    0x07:['d', 'D'],
    0x08:['e', 'E'],
    0x09:['f', 'F'],
    0x0A:['g', 'G'],
    0x0B:['h', 'H'],
    0x0C:['i', 'I'],
    0x0D:['j', 'J'],
    0x0E:['k', 'K'],
    0x0F:['l', 'L'],
    0x10:['m', 'M'],
    0x11:['n', 'N'],
    0x12:['o', 'O'],
    0x13:['p', 'P'],
    0x14:['q', 'Q'],
    0x15:['r', 'R'],
    0x16:['s', 'S'],
    0x17:['t', 'T'],
    0x18:['u', 'U'],
    0x19:['v', 'V'],
    0x1A:['w', 'W'],
    0x1B:['x', 'X'],
    0x1C:['y', 'Y'],
    0x1D:['z', 'Z'],
    0x1E:['1', '!'],
    0x1F:['2', '@'],
    0x20:['3', '#'],
    0x21:['4', '$'],
    0x22:['5', '%'],
    0x23:['6', '^'],
    0x24:['7', '&'],
    0x25:['8', '*'],
    0x26:['9', '('],
    0x27:['0', ')'],
    0x28:['\n','\n'],
    0x29:['[ESC]','[ESC]'],
    0x2a:['[BACKSPACE]', '[BACKSPACE]'],
    0x2C:[' ', ' '],
    0x2D:['-', '_'],
    0x2E:['=', '+'],
    0x2F:['[', '{'],
    0x30:[']', '}'],
    0x32:['#','~'],
    0x33:[';', ':'],
    0x34:['\'', '"'],
    0x36:[',', '<'],
    0x37:['.', '>'],
    0x38:['/', '?'],
    0x39:['[CAPSLOCK]','[CAPSLOCK]'],
    0x2b:['\t','\t'],
    0x4f:[u'→',u'→'],
    0x50:[u'←',u'←'],
    0x51:[u'↓',u'↓'],
    0x52:[u'↑',u'↑']
}

def read_use(capdatas):
    datas = [d.strip() for d in capdatas if d] 
    cursor_x = 0
    cursor_y = 0
    offset_current_line = 0
    lines = []
    output = ''
    skip_next = False
    lines.append("")
    for data in datas:
        shift = int(data.split(':')[0], 16) # 0x2 is left shift 0x20 is right shift
        key = int(data.split(':')[2], 16)

        if skip_next:
            skip_next = False
            continue
        
        if key == 0 or int(data.split(':')[3], 16) > 0:
            continue
        
        if shift != 0:
            shift=1
            skip_next = True
        
        if KEY_CODES[key][shift] == u'↑':
            lines[cursor_y] += output
            output = ''
            cursor_y -= 1
        elif KEY_CODES[key][shift] == u'↓':
            lines[cursor_y] += output
            output = ''
            cursor_y += 1
        elif KEY_CODES[key][shift] == u'→':
            cursor_x += 1
        elif KEY_CODES[key][shift] == u'←':
            cursor_x -= 1
        elif KEY_CODES[key][shift] == '\n':
            lines.append("")
            lines[cursor_y] += output
            cursor_x = 0
            cursor_y += 1
            output = ''
        elif KEY_CODES[key][shift] == '[BACKSPACE]':
            output = output[:-1]
            #lines[cursor_y] = output
            cursor_x -= 1
        else:
            output += KEY_CODES[key][shift]
            #lines[cursor_y] = output
            cursor_x += 1
    #print(lines)
    if lines == [""]:
        lines[0] = output
    if output != '' and output not in lines:
        lines[cursor_y] += output
    return '\n'.join(lines)

def parse_capdatas(file, devices) : 
    results = {}
    usb_keyboard_filter = "usb.capdata and usb.data_len==8"

    for device in devices : 
        apply_filter = f"{usb_keyboard_filter} and usb.src == {device}"
        capdatas = subprocess.run(["tshark", "-r", file, "-T", "fields", "-e", "usb.capdata", "-Y", apply_filter], capture_output=True, text=True)
        capdatas = capdatas.stdout.splitlines()
        capdatas = [":".join(s[i:i+2] for i in range(0, len(s), 2)) for s in capdatas]
        results[device] = capdatas if capdatas else "No packets matching USB HID definition."
    
    return results

def parse_arguments() :
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("file", type=str, help="path to pcap file.")
    parser.add_argument("-d", "--devices", type= str, nargs ="+", help="List of devices to extract keypresses")
    parser.add_argument("-r", "--render", type=str, choices=["csv", "json", "txt", "tab"], default="csv", help="Specify the output format. Available formats: %(choices)s. Default is %(default)s.")
    parser.add_argument("-e", "--extract", type=str, default=None, help="Save the results to the specified output file.")
    parser.add_argument("--index", action='store_true', default=False, help="Include an index column in the output (useful for CSV/JSON formats).")
    parser.add_argument("--no_space", action='store_true', help="Remove leading and trailing spaces from the output, useful for cleaner result processing.")
    parser.add_argument("-q","--quiet", action='store_true', default=False, help="Suppress the script's banner during execution.")
    args = parser.parse_args()
    return args

def main() :
    args = parse_arguments()
    banner(args.quiet)
    capdatas = parse_capdatas(args.file, args.devices)
    results = {"id":[], "result":[]}
    for device in args.devices : 
        if type(capdatas[device]) == list : 
            try : 
                res = read_use(capdatas[device])
            except : 
                res = "Failed to parse data, probably not a keyboard"
        else : 
            res = capdatas[device]
        results["id"].append(device)
        results["result"].append(res)

    df = pd.DataFrame(results)
    print("\n\n", df["result"][0], "\n")

if __name__ == "__main__" : 
    main()