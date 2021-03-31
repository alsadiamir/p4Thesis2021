
from scapy.all import *
import sys, os

TYPE_SENDTS = 0x1234
TYPE_IPV4 = 0x0800


class SendT(Packet):
    name = "OpProgram"
    fields_desc = [StrFixedLenField("P", "T", length=1),
                   LongField("ts",long(time.time()*1000000))]

bind_layers(Ether, SendT, type=TYPE_SENDTS)
bind_layers(SendT, IP, pid=TYPE_IPV4)
