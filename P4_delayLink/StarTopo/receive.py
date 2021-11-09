#!/usr/bin/env python
import sys
import struct
import os
os.sys.path.append('/home/prince7/.local/lib/python2.7/site-packages/')
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
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def handle_pkt(pkt):
    pkt.show2()
    if MyTunnel in pkt:
        print("got a packet")
        

        if (pkt.s11i > 0) and (pkt.s11e > 0) and (pkt.s21i > 0) and (pkt.s21e > 0) and (pkt.s51i > 0) and (pkt.s51e > 0) and (pkt.s31i > 0) and (pkt.s31e > 0) and (pkt.s4i > 0) and (pkt.s4e > 0) and (pkt.s32i > 0) and (pkt.s32e > 0) and (pkt.s52i > 0) and (pkt.s52e > 0) and (pkt.s22i > 0) and (pkt.s22e > 0) and (pkt.s12i > 0) and (pkt.s12e > 0):
            f = open(filenameS1,"a")
            f.write(str(pkt.s11i))
            f.write(",")
            f.write(str(pkt.s11e))
            f.write(",")
            f.write(str(pkt.s21i))
            f.write(",")
            f.write(str(pkt.s21e))
            f.write(",")
            f.write(str(pkt.s51i))
            f.write(",")
            f.write(str(pkt.s51e))
            f.write(",")
            f.write(str(pkt.s31i))
            f.write(",")
            f.write(str(pkt.s31e))
            f.write(",")
            f.write(str(pkt.s4i))
            f.write(",")
            f.write(str(pkt.s4e))
            f.write(",")
            f.write(str(pkt.s32i))
            f.write(",")
            f.write(str(pkt.s32e))
            f.write(",")
            f.write(str(pkt.s52i))
            f.write(",")
            f.write(str(pkt.s52e))
            f.write(",")
            f.write(str(pkt.s22i))
            f.write(",")
            f.write(str(pkt.s22e))
            f.write(",")
            f.write(str(pkt.s12i))
            f.write(",")
            f.write(str(pkt.s12e))
            f.write("\n")
            f.close()
            sys.stdout.flush()



def main():
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print("sniffing on %s" % iface)

    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
