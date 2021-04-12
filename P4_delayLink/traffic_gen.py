#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
import argparse
from datetime import datetime
import time

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, hexdump
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

sys.path.append(".")
from myTunnel_header import MyTunnel

delay = 10

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


    print "sending first packet on interface {} to dst_id {}".format(iface, str(2))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / MyTunnel(dst_id=2, flag_s=0) / IP(dst="10.0.1.1") / "TRAFFIC..."

    pkt.show2()
    while True :
        print "resending...."
        sendp(pkt, iface=iface, verbose=False)
        time.sleep(0.2)

if __name__ == '__main__':
    main()
