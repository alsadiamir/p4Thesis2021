#!/usr/bin/env python

import argparse
import sys
import socket
import random
import struct
import re
import time

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP, BCDFloatField, IntField, StrFixedLenField, IEEEFloatField, LongField
sys.path.append(".")
from SendT_header import SendT

import readline
from time import sleep

def get_ts():
    t = time.time()
    return t

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

    iface = get_if()
    #addr = socket.gethostbyname(sys.argv[1])

    print "sending on interface %s to s1" % (iface)
    pkt =  Ether(dst='00:01:00:00:00:00', type=0x1234)
    pkt = pkt  / SendT(ts=long(get_ts()*1000000))
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
