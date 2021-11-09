import os
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=False, default='simple_switch' )
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=2)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)

args = parser.parse_args()

class SingleSwitchTopo(Topo):
    def __init__(self, sw_path, json_path, thrift_port, pcap_dump, **opts):
        Topo.__init__(self, **opts)

        switch1 = self.addSwitch('s1', sw_path = sw_path, json_path = json_path, thrift_port = 9090,cls = P4Switch ,pcap_dump = pcap_dump)
        switch2 = self.addSwitch('s2', sw_path = sw_path, json_path = json_path, thrift_port = 9091,cls = P4Switch ,pcap_dump = pcap_dump)
        switch3 = self.addSwitch('s3', sw_path = sw_path, json_path = json_path, thrift_port = 9092,cls = P4Switch ,pcap_dump = pcap_dump)
        switch4 = self.addSwitch('s4', sw_path = sw_path, json_path = json_path, thrift_port = 9093,cls = P4Switch ,pcap_dump = pcap_dump)
        switch5 = self.addSwitch('s5', sw_path = sw_path, json_path = json_path, thrift_port = 9094,cls = P4Switch ,pcap_dump = pcap_dump)

        host1 = self.addHost('h1',ip='10.0.1.1')
        host2 = self.addHost('h2',ip='10.0.1.2')

        self.addLink(host1, switch1, port1=0,port2=1)
        self.addLink(host2, switch1, port1=0,port2=4)
        self.addLink(switch1, switch2, port1=2,port2=1, delay="100ms")
        self.addLink(switch2, switch5, port1=2,port2=1, delay="100ms")
        self.addLink(switch5, switch3, port1=2,port2=1, delay="100ms")
        self.addLink(switch3, switch4, port1=2,port2=1, delay="100ms")
        self.addLink(switch4, switch5, port1=2,port2=3)
        self.addLink(switch5, switch1, port1=4,port2=3)

def main():
    topo = SingleSwitchTopo(args.behavioral_exe, args.json, args.thrift_port, args.pcap_dump)
    #controller1 = RemoteController('controller1', ip = '10.108.148.148')
    net = Mininet(topo=topo,
                   host=P4Host, link=TCLink,
                   autoStaticArp=True, controller = None)
    net.start()

    sleep(1)

    print('\033[0;32m'),
    print('Gotcha!')
    print('\033[0m')

    CLI(net)
    try:
        net.stop()
    except:
        print('\033[0;31m'),
        print('Stop error! Trying sudo mn -c')
        print('\033[0m')
        os.system('sudo mn -c')
        print('\033[0;32m'),
        print ('Stop successfully!')
        print('\033[0m')

if __name__ == '__main__':
    setLogLevel('info')
    main()
