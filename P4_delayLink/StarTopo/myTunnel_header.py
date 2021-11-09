
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
        BitField("s11i",0,48),
        BitField("s11e",0,48), 
        BitField("s21i",0,48),
        BitField("s21e",0,48),
        BitField("s51i",0,48),
        BitField("s51e",0,48),
        BitField("s31i",0,48),
        BitField("s31e",0,48),
        BitField("s4i",0,48),
        BitField("s4e",0,48),
        BitField("s32i",0,48),
        BitField("s32e",0,48),
        BitField("s52i",0,48),
        BitField("s52e",0,48),
        BitField("s22i",0,48),
        BitField("s22e",0,48),
        BitField("s12i",0,48),
        BitField("s12e",0,48)]


bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)

bind_layers(MyTunnel, IP, pid=TYPE_IPV4)
