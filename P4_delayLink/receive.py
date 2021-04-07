#!/usr/bin/env python
import sys
import struct
import os
from datetime import datetime

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR

sys.path.append(".")
from myTunnel_header import MyTunnel

filenameS1 = "dataS1.csv"
filenameS2 = "dataS2.csv"

def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def handle_pkt(pkt):
    if MyTunnel in pkt:
        print "got a packet"

        if (pkt.ts_ing > 0) and (pkt.ts_eg > 0) :
            pkt.show2()
            if pkt.flag_s == 0 :
                f = open(filenameS1,"a")
            if pkt.flag_s == 1 :
                f = open(filenameS2,"a")

            f.write(str(pkt.ts_ing))
            f.write(",")
            f.write(str(pkt.ts_eg))
            f.write("\n")
            f.close()
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
