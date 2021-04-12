import statistics
D = 30000 #micros
s1 = open("dataS1_30ms_withtraffic.csv","r")
s2 = open("dataS2_30ms_withtraffic.csv","r")


s1_m = 0.0
s2_m = 0.0
t_m = 0.0
owd_m = 0.0
index = 0
var_owd = []

s1r = s1.readline()
s2r = s2.readline()
while (s1r != "") and (s2r != ""):
    s1r_ts = s1r.split(",")
    s2r_ts = s2r.split(",")
    if(len(s1r_ts) >=2) and (len(s2r_ts) >=2):
        I1 = float(s1r_ts[0])
        E2 = float(s1r_ts[1])
        E1 = float(s2r_ts[1])
        I2 = float(s2r_ts[0])
        s1_m += E1 - I1 - D
        s2_m += E2 - I2 + D
        t_m += E2 - I1 + D
        owd_m += I2 - E1 + D
        var_owd.append(I2 - E1 + D)
        index += 1
    s1r = s1.readline()
    s2r = s2.readline()


s1_m = s1_m/float(index)
print "ts1 medio = "+ str(s1_m) + " micros"

s2_m = s2_m/float(index)
print "ts2 medio = "+ str(s2_m) + " micros"

t_m = t_m/float(index)
print "t medio = "+ str(t_m) + " micros"

owd_m = owd_m/float(index)
print "owd medio = "+ str(owd_m) + " micros"

print "owd's: "+str(var_owd)

print "variance = " + str(statistics.variance(var_owd))

s1.close();
s2.close();
