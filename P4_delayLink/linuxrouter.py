#!/usr/bin/env python

"""
linuxrouter.py: Example network with Linux IP router
This example converts a Node into a router using IP forwarding
already built into Linux.
The example topology creates a router and three IP subnets:
    - 192.168.1.0/24 (r0-eth1, IP: 192.168.1.1)
    - 172.16.0.0/12 (r0-eth2, IP: 172.16.0.1)
    - 10.0.0.0/8 (r0-eth3, IP: 10.0.0.1)
Each subnet consists of a single host connected to
a single switch:
    r0-eth1 - s1-eth1 - h1-eth0 (IP: 192.168.1.100)
    r0-eth2 - s2-eth1 - h2-eth0 (IP: 172.16.0.100)
    r0-eth3 - s3-eth1 - h3-eth0 (IP: 10.0.0.100)
The example relies on default routing entries that are
automatically created for each router interface, as well
as 'defaultRoute' parameters for the host interfaces.
Additional routes may be added to the router or hosts by
executing 'ip route' or 'route' commands on the router or hosts.
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    # pylint: disable=arguments-differ
    def build( self, **_opts ):

        defaultIP = '10.0.1.0/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )

        s1 = self.addSwitch('s1', sw_path = "/home/vagrant/behavioral-model/targets/simple_switch/simple_switch", json_path = "basic.json", thrift_port = 9090,cls = P4Switch ,pcap_dump = False)
        s2 = self.addSwitch('s2', sw_path = "/home/vagrant/behavioral-model/targets/simple_switch/simple_switch", json_path = "basic.json", thrift_port = 9091,cls = P4Switch ,pcap_dump = False)
        s3 = self.addSwitch('s3', sw_path = "/home/vagrant/behavioral-model/targets/simple_switch/simple_switch", json_path = "basic.json", thrift_port = 9092,cls = P4Switch ,pcap_dump = False)

        self.addLink( s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIP } )  # for clarity
        self.addLink( s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '10.0.2.0/12' } )
        self.addLink( s3, router, intfName2='r0-eth3',
                      params2={ 'ip' : '10.0.3.0/8' } )


        h1 = self.addHost( 'h1', ip='10.0.1.1/24',
                           defaultRoute='via 10.0.1.0' )
        h2 = self.addHost( 'h2', ip='10.0.2.2/12',
                           defaultRoute='via 10.0.2.0' )
        h3 = self.addHost( 'h3', ip='10.0.3.3/8',
                           defaultRoute='via 10.0.3.0' )

        self.addLink(h1, s1)
        self.addLink(s1, s2, delay='1s',  use_htb=True)
        self.addLink(s1, s3)
        self.addLink(s3, s2)
        self.addLink(s2, h2)
        self.addLink(s3, h3)



def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
