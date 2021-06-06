
from scapy.all import *
import sys, os

TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800

class MyTunnel(Packet):
    name = "MyTunnel"
    fields_desc = [
        ShortField("pid", 0), #Protocol ID
        ShortField("dst_id", 0), #Destination Port
        ShortField("nhop", 0), #Flag to track the packet route
        BitField("ts_ing1",0,48), #timestamp of ingress1 queue
        BitField("ts_eg1",0,48),  #timestamp of egress1 queue
        BitField("ts_is2",0,48), #timestamp of ingress1 queue
        BitField("ts_es2",0,48),  #timestamp of egress1 queue
        BitField("ts_ing2",0,48), #timestamp of ingress2 queue
        BitField("ts_eg2",0,48)] #timestamp of egress2 queue


bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)
bind_layers(MyTunnel, IP, pid=TYPE_IPV4)
