#!/usr/bin/env python

import argparse
import sys
import socket
import random
import struct
import re

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP, StrFixedLenField, XByteField, IntField

import readline

class OpProgram(Packet):
    name = "OpProgram"
    fields_desc = [StrFixedLenField("P", "P", length=1),
                   IntField("operation", 0)]

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def main():

    if len(sys.argv) < 2:
        print 'pass 1 arguments: "<cmd>"'
        exit(1)

    iface = get_if()

    print "sending on interface %s to s1" % (iface)
    pkt =  Ether(dst='00:01:00:00:00:00', type=0x1234)
    pkt = pkt  / OpProgram(operation=int(sys.argv[1]))
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
