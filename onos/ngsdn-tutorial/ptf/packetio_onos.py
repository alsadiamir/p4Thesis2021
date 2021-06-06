#!/usr/bin/env python2
import argparse
import grpc
import os
import sys


# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 './utils/'))
import p4runtime_lib.bmv2
from p4runtime_lib.switch import ShutdownAllSwitchConnections
import p4runtime_lib.helper
from base_test import *

CPU_CLONE_SESSION_ID = 99
TYPE_MYTUNNEL = 0x1212

SWITCH_TO_HOST_PORT = 1
SWITCH_TO_SWITCH_PORT = 2

def runTest():
    dst_id = 2
    eth_dst='00:dd:00:00:00:01'
    eth_src='00:00:00:00:00:10'
    pkt = testutils.scapy.Ether(dst=eth_dst, src=eth_src, type=TYPE_MYTUNNEL)
    pkt = pkt / MyTunnel(dst_id=dst_id) / 'ping'
    self.testPacket(pkt)

def writeTunnelPacket(p4info_helper, sw,
                     dst_eth_addr, dst_ip_addr):
    P4RuntimeTest.insert_pre_clone_session(
        session_id=CPU_CLONE_SESSION_ID,
        ports=[self.cpu_port])
    outport=2
    packet_out_msg = P4RuntimeTest.helper.build_packet_out(
        payload=str(pkt),
        metadata={
            "egress_port": outport,
            "_pad": 0
        })
    P4RuntimeTest.send_packet_out(packet_out_msg)


def printGrpcError(e):
    print("gRPC Error:", e.details()),
    status_code = e.code()
    print("(%s)" % status_code.name),
    traceback = sys.exc_info()[2]
    print("[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))

def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:
        # Create a switch connection object for s1 and s2;
        # this is backed by a P4Runtime gRPC connection.
        # Also, dump all P4Runtime messages sent to switch to given txt files.
        leaf1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='leaf1',
            address='127.0.0.1:50001',
            device_id=1,
            proto_dump_file='logs/s1-p4runtime-requests.txt')

        leaf1.MasterArbitrationUpdate()

        # Install the P4 program on the switches
        leaf1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on leaf1")


        # Write the rules that tunnel traffic from h1 to h2
        writeTunnelPacket()

    except KeyboardInterrupt:
        print(" Shutting down.")
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced_tunnel.p4.p4info.txt')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced_tunnel.json')
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file not found: %s\nHave you run 'make'?" % args.p4info)
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print ("\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json)
        parser.exit(1)
    main(args.p4info, args.bmv2_json)
