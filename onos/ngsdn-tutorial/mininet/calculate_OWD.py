#!/usr/bin/env python
"""
 h1--S1--S2--S4--h4
      \  /
       S3
Probe is sent from h4 to h1
Path measured: S2-S3
Path taken from the probe: h4->S4->S2->S3->S2->S1->h1
How the RTT is measured:
(egress S1(second time the probe goes through it) - ingress S1(the first time the probe passes through it) - RS1_2)
How the OWD is measured:
(RTT - RS1_1 - RS2) / 2

"""


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help='The file from which the OWD is calculated - line format must be (6 entries): ts_ingress_rs1_1,ts_egress_rs1_1,ts_ingress_rs2,ts_egress_rs2,ts_ingress_rs1_2,ts_egress_rs1_2')
args = parser.parse_args()

s1 = open(args.f,"r")
s1_m = 0.0
s2_m = 0.0
rtt_m = 0.0
owd_m = 0.0
index = 0
var_owd = []

s1r = s1.readline()
while (s1r != ""):
    s1r_ts = s1r.split(",")
    if(len(s1r_ts) >=6):
        I1 = float(s1r_ts[0])
        E1 = float(s1r_ts[1])
        IS2 = float(s1r_ts[2])
        ES2 = float(s1r_ts[3])
        I2 = float(s1r_ts[4])
        E2 = float(s1r_ts[5])
        rs1_1 = E1 - I1
        rs1_2 = E2 - I2
        rs2 = ES2 - IS2
        rtt = E2 - I1 - rs1_2
        owd = (rtt - rs2 - rs1_2) / 2
        s1_m += (rs1_1 + rs1_2) / 2
        s2_m += rs2
        rtt_m += rtt
        owd_m += owd
        var_owd.append(owd)
        index += 1
    s1r = s1.readline()


s1_m = s1_m/float(index)
print "rs1 medio = "+ str(s1_m) + " micros"

s2_m = s2_m/float(index)
print "rs2 medio = "+ str(s2_m) + " micros"

rtt_m = rtt_m/float(index)
print "rtt medio = "+ str(rtt_m) + " micros"

owd_m = owd_m/float(index)
print "owd medio = "+ str(owd_m) + " micros"

print "owd's: "+str(var_owd)

#print "variance = " + str(statistics.variance(var_owd))

s1.close();
