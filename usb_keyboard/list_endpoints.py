import subprocess
import pandas as pd
from collections import defaultdict

# Protocol options for get_endpoints according to tshark doc: 
#
# "bluetooth" Bluetooth addresses
# "dccp"      DCCP/IP socket pairs Both IPv4 and IPv6 are supported
# "eth"       Ethernet addresses
# "fc"        Fibre Channel addresses
# "fddi"      FDDI addresses
# "ip"        IPv4 addresses
# "ipv6"      IPv6 addresses
# "ipx"       IPX addresses
# "jxta"      JXTA message addresses
# "mptcp"     Multipath TCP connections
# "ncp"       NCP connections
# "rsvp"      RSVP connections
# "sctp"      SCTP/IP socket pairs Both IPv4 and IPv6 are supported
# "sll"       Linux "cooked mode" capture addresses
# "tcp"       TCP/IP socket pairs  Both IPv4 and IPv6 are supported
# "tr"        Token Ring addresses
# "udp"       UDP/IP socket pairs  Both IPv4 and IPv6 are supported
# "usb"       USB addresses
# "wlan"      IEEE 802.11 addresses
# "wpan"      IEEE 802.15.4 addresses
# "zbee_nwk"  ZigBee Network Layer addresses

def get_endpoints(file, protocol):
    result = subprocess.run(["tshark", "-r", file, "-q", "-z", f"endpoints,{protocol}"], capture_output=True, text=True)
    lines = result.stdout.splitlines()[4:-1]
    data = [line.split() for line in lines if len(line.split()) >= 6]
    df = pd.DataFrame(data, columns=["address", "packets", "_", "tx_packets", "_", "rx_packets", "_"]).drop(columns=["_", "_"])
    df[["packets", "tx_packets", "rx_packets"]] = df[["packets", "tx_packets", "rx_packets"]].astype(int)
    return df

def get_protocols(file):
    result = subprocess.run(["tshark", "-r", file, "-q", "-z", "io,phs"], capture_output=True, text=True)
    lines = result.stdout.splitlines()[5:-1] 
    protocols = [line.split()[0] for line in lines if line and line[0] != " "]
    return protocols

# def check_if_any_keyboard(file, devices):
    keyboards = defaultdict(int)

    # 1. Identifier les devices ayant usb.data_len == 8 et usb.capdata[1] == 00
    filter_expr = "usb.data_len == 8 and usb.capdata[1] == 00"
    cmd_result = subprocess.run(["tshark", "-r", file, "-Y", filter_expr], capture_output=True, text=True)

    # Remplissage du dictionnaire keyboards
    for line in cmd_result.stdout.splitlines():
        pkt = line.split()
        if len(pkt) >= 3:  # Sécurité pour éviter les erreurs d'index
            keyboards[pkt[2]] += 1

    # 2. Vérifier la correspondance avec le nombre de paquets attendus
    keyboards = {d: count for d, count in keyboards.items() if count == devices.get(d, [0, 0])[1]}

    # 3. Vérifier si les devices ont des rapports nuls
    valid_keyboards = []
    for keyboard in keyboards:
        null_filter = f"usb.capdata[0:8] == 00:00:00:00:00:00:00:00 and usb.addr == {keyboard}"
        cmd_result = subprocess.run(["tshark", "-r", file, "-Y", null_filter], capture_output=True, text=True)

        if cmd_result.stdout.strip():  # Vérifie s'il y a des résultats
            valid_keyboards.append(keyboard)

    return valid_keyboards

def check_if_any_keyboard(file, devices):
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

        # Vérifier la présence de rapports nuls (usb.capdata[0:8] == 00:00:00:00:00:00:00:00)
        if capdata == "0000000000000000":
            null_reports.add(device_id)

    # Filtrer les devices valides (ceux qui ont le bon nombre de paquets et des rapports nuls)
    valid_keyboards = [
        d for d in keyboards
        if keyboards[d] == devices.get(d, [0, 0])[1] 
        and d in null_reports
    ]

    return valid_keyboards


file = "/Users/emrehancil/Desktop/FORENSIC1/klogger.pcapng"
protocol = "usb"

protocols = get_protocols(file)
endpoints = get_endpoints(file, protocol)
T_endpoints = endpoints.set_index("address").T.reset_index(drop=True)
keyboards = check_if_any_keyboard(file, T_endpoints)

print(protocols)
print(endpoints)
print(keyboards)
