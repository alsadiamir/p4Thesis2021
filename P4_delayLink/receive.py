#!/usr/bin/env python
import sys
import struct
import os
import argparse
from datetime import datetime

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR

sys.path.append(".")
from myTunnel_header import MyTunnel

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help='The file in which entries are saved - line format is (6 entries): ts_ingress_rs1_1,ts_egress_rs1_1,ts_ingress_rs2,ts_egress_rs2,ts_ingress_rs1_2,ts_egress_rs1_2')
args = parser.parse_args()

filenameS1 = args.f

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
        pkt.show2()

        if (pkt.ts_ing1 > 0) and (pkt.ts_eg1 > 0) and (pkt.ts_is2 > 0) and (pkt.ts_es2 > 0) and (pkt.ts_ing2 > 0) and (pkt.ts_eg2 > 0):
            f = open(filenameS1,"a")
            f.write(str(pkt.ts_ing1))
            f.write(",")
            f.write(str(pkt.ts_eg1))
            f.write(",")
            f.write(str(pkt.ts_is2))
            f.write(",")
            f.write(str(pkt.ts_es2))
            f.write(",")
            f.write(str(pkt.ts_ing2))
            f.write(",")
            f.write(str(pkt.ts_eg2))
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
