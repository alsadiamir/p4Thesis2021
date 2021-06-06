#!/usr/bin/env python
# Copyright 2019-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# ------------------------------------------------------------------------------
# CONTROLLER PACKET-IN/OUT TESTS
#
# To run all tests in this file:
#     make p4-test TEST=packetio
#
# To run a specific test case:
#     make p4-test TEST=packetio.<TEST CLASS NAME>
#
# For example:
#     make p4-test TEST=packetio.PacketOutTest
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Modify everywhere you see TODO
#
# When providing your solution, make sure to use the same names for P4Runtime
# entities as specified in your P4Info file.
#
# Test cases are based on the P4 program design suggested in the exercises
# README. Make sure to modify the test cases accordingly if you decide to
# implement the pipeline differently.
# ------------------------------------------------------------------------------

import sys
sys.path.append(".")
from myTunnel_header import MyTunnel
from ptf.testutils import group
from base_test import *

CPU_CLONE_SESSION_ID = 99
TYPE_MYTUNNEL = 0x1212

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

@group("my_tunnel_packetio")
class PacketOutTest(P4RuntimeTest):
    #Tests controller packet-out capability by sending PacketOut messages and
    #expecting a corresponding packet on the output port set in the PacketOut
    #metadata.

    def runTest(self):
        dst_id = 2
        eth_dst='00:dd:00:00:00:01'
        eth_src='00:00:00:00:00:10'
        #print "sending PROBE on interface {} to dst_id {}".format(iface, str(dst_id))
        #pkt =  Ether(src=get_if_hwaddr(iface), dst='00:dd:00:00:00:01')
        pkt = testutils.scapy.Ether(dst=eth_dst, src=eth_src, type=TYPE_MYTUNNEL)
        pkt = pkt / MyTunnel(dst_id=dst_id) / 'ping'
        self.testPacket(pkt)

    def testPacket(self, pkt):

        self.insert_pre_clone_session(
            session_id=CPU_CLONE_SESSION_ID,
            ports=[self.cpu_port])
        outport=2
        packet_out_msg = self.helper.build_packet_out(
            payload=str(pkt),
            metadata={
                "egress_port": outport,
                "_pad": 0
            })
        self.send_packet_out(packet_out_msg)

        #timeout = None
        #if timeout==None:
        #    timeout=ptf.ptfutils.default_timeout
        #device, port = testutils.port_to_tuple(outport)
        #print "Checking for pkt on device ",device,", port ", port
        #result = testutils.dp_poll(self, device_number=device, port_number=port,
        #         timeout=timeout, exp_pkt=pkt)

        testutils.verify_packet(self, pkt, outport)
        #result = self.get_packet_in()
        #print(result.format())

"""
@group("my_tunnel_packetio")
class PacketInTest(P4RuntimeTest):

#    Tests controller packet-in capability my matching on the packet EtherType
#    and cloning to the CPU port.

    def runTest(self):
        dst_id = 2
        iface = get_if()
        print "sending PROBE on interface {} to dst_id {}".format(iface, str(dst_id))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='00:00:00:00:00:10')
        pkt = pkt / MyTunnel(dst_id=dst_id) / IP(dst = "10.0.1.1") / "ping"
        self.testPacket(pkt)

    @autocleanup
    def testPacket(self, pkt):

        for inport in [self.port1, self.port2, self.port3]:
            exp_packet_in_msg = self.helper.build_packet_in(
                payload=str(pkt),
                metadata={
                    "ingress_port": inport,
                    "_pad": 0
                })

            timeout = None
            if timeout==None:
                timeout=ptf.ptfutils.default_timeout
            device, port = testutils.port_to_tuple(inport)

            logging.debug("Checking for pkt on device %d, port %d", device, port)
            result = testutils.dp_poll(self, device_number=device, port_number=port,
                                       timeout=timeout, exp_pkt=pkt)
            print(result.format())
"""