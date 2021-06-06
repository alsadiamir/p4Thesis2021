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
# IPV6 ROUTING TESTS
#
# To run all tests:
#     make p4-test TEST=routing
#
# To run a specific test case:
#     make p4-test TEST=routing.<TEST CLASS NAME>
#
# For example:
#     make p4-test TEST=routing.IPv6RoutingTest
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

@group("my_tunnel_routing")
class IPv6RoutingTest(P4RuntimeTest):
    #Tests basic IPv6 routing

    def runTest(self):
        dst_id = 2
        iface = get_if()
        print "sending PROBE on interface {} to dst_id {}".format(iface, str(dst_id))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='00:00:00:00:00:10')
        pkt = pkt / MyTunnel(dst_id=dst_id) / IPv6(dst = "2001:1:1::1") / "ping"
        #pkt.show2()
        self.testPacket(pkt)

    @autocleanup
    def testPacket(self, pkt):
        next_hop_mac = '00:dd:00:00:00:01'
        print_inline("MAC= %s ... " % next_hop_mac)
        print_inline("PORT1= %d ... " % self.port1)
        print_inline("PORT2= %d ... " % self.port2)
        # Add entry to "My Station" table. Consider the given pkt's eth dst addr
        # as myStationMac address.
        # *** TODO EXERCISE 5
        # Modify names to match content of P4Info file (look for the fully
        # qualified name of tables, match fields, and actions.
        # ---- START SOLUTION ----
        self.insert(self.helper.build_table_entry(
            table_name="IngressPipeImpl.my_station_table",
            match_fields={
                # Exact match.
                "hdr.ethernet.dst_addr": pkt[Ether].dst
            },
            action_name="NoAction"
        ))
        # ---- END SOLUTION ----

        # Insert ECMP group with only one member (next_hop_mac)
        # *** TODO EXERCISE 5
        # Modify names to match content of P4Info file (look for the fully
        # qualified name of tables, match fields, and actions.
        # ---- START SOLUTION ----
        self.insert(self.helper.build_act_prof_group(
            act_prof_name="IngressPipeImpl.ecmp_selector",
            group_id=1,
            actions=[
                # List of tuples (action name, action param dict)
                ("IngressPipeImpl.set_next_hop", {"dmac": next_hop_mac}),
            ]
        ))
        # ---- END SOLUTION ----

        # Insert L3 routing entry to map pkt's IPv6 dst addr to group
        # *** TODO EXERCISE 5
        # Modify names to match content of P4Info file (look for the fully
        # qualified name of tables, match fields, and actions.
        # ---- START SOLUTION ----
        self.insert(self.helper.build_table_entry(
            table_name="IngressPipeImpl.routing_v6_table",
            match_fields={
                # LPM match (value, prefix)
                "hdr.ipv6.dst_addr": (pkt[IPv6].dst, 128)
            },
            group_id=1
        ))
        # ---- END SOLUTION ----

        # Insert L3 entry to map next_hop_mac to output port 2.
        # *** TODO EXERCISE 5
        # Modify names to match content of P4Info file (look for the fully
        # qualified name of tables, match fields, and actions.
        # ---- START SOLUTION ----
        self.insert(self.helper.build_table_entry(
            table_name="IngressPipeImpl.l2_exact_table",
            match_fields={
                # Exact match
                "hdr.ethernet.dst_addr": next_hop_mac
            },
            action_name="IngressPipeImpl.set_egress_port",
            action_params={
                "port_num": self.port2
            }
        ))
        # ---- END SOLUTION ----

        # Expected pkt should have routed MAC addresses and decremented hop
        # limit (TTL).
        exp_pkt = pkt.copy()
        pkt_route(exp_pkt, next_hop_mac)
        pkt_decrement_ttl(exp_pkt)

        testutils.send_packet(self, self.port1, str(pkt))
        testutils.verify_packet(self, exp_pkt, self.port2)
