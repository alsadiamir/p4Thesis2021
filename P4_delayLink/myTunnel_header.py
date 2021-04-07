
from scapy.all import *
import sys, os

TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800

class MyTunnel(Packet):
    name = "MyTunnel"
    fields_desc = [
        ShortField("pid", 0), #Protocol ID
        ShortField("dst_id", 0), #Destination Port
        ShortField("flag_s", 0), #Flag to assign the switch
        ShortField("nhop", 0), #Flag to track the packet route
        BitField("ts_ing",0,48), #timestamp of ingress queue
        BitField("ts_eg",0,48)]  #timestamp of egress queue


bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)
bind_layers(MyTunnel, IP, pid=TYPE_IPV4)
