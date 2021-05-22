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
    #time.sleep(delay)
    TYPE_MYTUNNEL = 0x1212
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_addr', type=str, help="The destination IP address to use")
    parser.add_argument('message', type=str, help="The message to include in packet")
    parser.add_argument('--dst_id', type=int, default=None, help='The myTunnel dst_id to use, if unspecified then myTunnel header will not be included in packet')

    args = parser.parse_args()

    addr = socket.gethostbyname(args.ip_addr)
    dst_id = args.dst_id

    iface = get_if()
    pkt1 = 0
    #time.sleep(delay)

    if (dst_id is not None):
        print "sending PROBE on interface {} to dst_id {}".format(iface, str(dst_id))
        # src=get_if_hwaddr(iface),
        pkt =  Ether(dst='ff:ff:ff:ff:ff:ff', type=TYPE_MYTUNNEL)
        pkt = pkt / MyTunnel(dst_id=dst_id) # / IP(dst=addr) / args.message
        print len(pkt)

    else:
        print "sending on interface {} to IP addr {}".format(iface, str(addr))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='00:dd:00:00:00:01')
        pkt = pkt / IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / args.message

    pkt.show2()

    sendp(pkt, iface=iface, verbose=False)

    #pkt1.show2()


if __name__ == '__main__':
    main()
