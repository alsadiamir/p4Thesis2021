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


filename = "data_millisecs.csv"

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
    if TCP in pkt:
        f = open(filename,"a")

        pkt.show2()
        print type(pkt.load)
        tsstart = long(pkt.load)
        print tsstart
        diff = time.time()*1000000-tsstart
        print diff

        if pkt.ttl > 0:
            f.write(str(diff))
            f.write(",")
            f.write(str(float(diff) / float(pkt.ttl)))
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
