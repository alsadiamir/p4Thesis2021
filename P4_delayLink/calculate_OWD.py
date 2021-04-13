import statistics
s1 = open("data_50ms_br.csv","r")

s1_m = 0.0
s2_m = 0.0
t_m = 0.0
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
        rs1 = ((E1 - I1) + (E2 - I2)) / 2
        rs2 = ES2 - IS2
        t = ( E2 - I1 - rs2 ) / 2
        owd = (E2 - I1 - rs2 - rs1) / 2
        s1_m += rs1
        s2_m += rs2
        t_m += t
        owd_m += owd
        var_owd.append(owd)
        index += 1
    s1r = s1.readline()


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
