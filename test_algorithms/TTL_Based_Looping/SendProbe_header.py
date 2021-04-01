
from scapy.all import *
import sys, os

TYPE_SENDTS = 0x1234
TYPE_IPV4 = 0x0800


class SendProbe(Packet):
    name = "OpProgram"
    fields_desc = [StrFixedLenField("P", "T", length=1),
                   LongField("ts",long(time.time()*1000000)),
                   IntField("it",0)]

bind_layers(Ether, SendProbe, type=TYPE_SENDTS)
bind_layers(SendProbe, IP, pid=TYPE_IPV4)
