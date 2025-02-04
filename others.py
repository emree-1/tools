
import subprocess
import pandas as pd

def get_protocols(file):
    result = subprocess.run(["tshark", "-r", file, "-q", "-z", "io,phs"], capture_output=True, text=True)
    lines = result.stdout.splitlines()[5:-1] 
    protocols = [line.split()[0] for line in lines if line and line[0] != " "]
    return protocols

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