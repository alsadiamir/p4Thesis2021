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


import statistics
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
    if(len(s1r_ts) >=18):
        I11 = float(s1r_ts[0])
        E11 = float(s1r_ts[1])
        I21 = float(s1r_ts[2])
        E21 = float(s1r_ts[3])
        I51 = float(s1r_ts[4])
        E51 = float(s1r_ts[5])
        I31 = float(s1r_ts[6])
        E31 = float(s1r_ts[7])
        I4 = float(s1r_ts[8])
        E4 = float(s1r_ts[9])
        I32 = float(s1r_ts[10])
        E32 = float(s1r_ts[11])
        I52 = float(s1r_ts[12])
        E52 = float(s1r_ts[13])
        I22 = float(s1r_ts[14])
        E22 = float(s1r_ts[15])
        I12 = float(s1r_ts[16])
        E12 = float(s1r_ts[17])

        s11 = E11 - I11
        s21 = E21 - I21
        s51 = E51 - I51
        s31 = E31 - I31
        s4 = E4 - I4
        s32 = E32 - I32
        s52 = E52 - I52
        s22 = E22 - I22
        s12 = E12 - I12

        allSwitches = s11 + s12 + s21 + s22 + s31 + s32 + s4 + s51 + s52
        
        rttWithComp = E12 - I11
        owd = (rttWithComp - allSwitches) / 2
        #s1_m += (rs1_1 + rs1_2) / 2
        #s2_m += rs2
        rtt_m += rttWithComp
        owd_m += owd
        var_owd.append(owd)
        index += 1
    s1r = s1.readline()

"""
s1_m = s1_m/float(index)
print "rs1 medio = "+ str(s1_m) + " micros"

s2_m = s2_m/float(index)
print "rs2 medio = "+ str(s2_m) + " micros"
"""

rtt_m = rtt_m/float(index)
print "rtt medio = "+ str(rtt_m) + " micros"

owd_m = owd_m/float(index)
print "owd medio = "+ str(owd_m) + " micros"

print "owd's: "+str(var_owd)

#print "variance = " + str(statistics.variance(var_owd))

s1.close()
