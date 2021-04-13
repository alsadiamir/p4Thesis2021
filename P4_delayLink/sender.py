#!/usr/bin/python3

import socket
from sys import argv
import os
import time

default_host = "localhost"
portnum = 5431
blockcount = 1000
cong_algorithm = 'reno'


def talk():
    global portnum, blockcount, cong_algorithm
    rhost = default_host
    if len(argv) > 1:
        blockcount = int(argv[1])
    if len(argv) > 2:
        rhost = argv[2]
    if len(argv) > 3:
        portnum = int(argv[3])
    if len(argv) > 4:
        cong_algorithm = argv[4]
    print("Looking up address of " + rhost + "...", end="")
    try:
        dest = socket.gethostbyname(rhost)
    except socket.gaierror as mesg:
        errno,errstr=mesg.args
        print("\n   ", errstr);
        return;
    print("got it: " + dest)
    addr=(dest, portnum)
    s = socket.socket()
    #IPPROTO_TCP = 6        	# defined in /usr/include/netinet/in.h
    TCP_CONGESTION = 13 	# defined in /usr/include/netinet/tcp.h
    cong = bytes(cong_algorithm, 'ascii')
    try:
       s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, cong)
    except OSError as mesg:
       errno, errstr = mesg.args
       print ('congestion mechanism {} not available: {}'.format(cong_algorithm, errstr))
       return
    res=s.connect_ex(addr)
    if res!=0: 
        print("connect to port ", portnum, " failed")
        return

    buf = bytearray(os.urandom(1000))
    starttime = time.time()
    for i in range(blockcount):
        s.send(buf)
    s.close()
    print('total time: {} seconds'.format(time.time()-starttime))

        
talk()
