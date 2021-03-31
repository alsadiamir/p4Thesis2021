#!/usr/bin/env python
import sys
import struct
import os
from datetime import datetime
import time

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField, IEEEFloatField
from scapy.all import IP, TCP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR

sys.path.append(".")

from SendProbe_header import SendProbe


filename = "data_nanosecs.csv"

def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def handle_pkt(pkt):
    #print "got a packet!!"
    if SendProbe in pkt or (TCP in pkt and pkt[TCP].dport == 1234):
        if pkt.it > 0:
            f = open(filename,"a")
            print "got a packet,flag = "+str(pkt.P)

            pkt.show2()
            tsarr = long(time.time()*1000000)
            print tsarr
            diff = tsarr-pkt.ts
            print diff

            f.write(str(diff))
            f.write(",")
            f.write(str(float(diff) / float(pkt.it)))
            f.write(",")

	f.close();
    sys.stdout.flush()



def main():
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print "sniffing on %s" % iface

    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
