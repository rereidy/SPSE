import sys
import scapy
from scapy.all import *

interface = sys.argv[1] 
unique = []

def sniffNonBeacon(p):
    if not p.haslayer(Dot11Beacon):
        if unique.count(p.addr2) == 0:
            unique.append(p.addr2)
    
    print p.sprintf("[%Dot11.addr1%][%Dot11.addr2%][%Dot11Elt.info%]")
    print p.summary()

sniff(iface=interface, prn=sniffNonBeacon)
