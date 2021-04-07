s1 = open("dataS1.csv","r")
s2 = open("dataS2.csv","r")


s1_m = 0.0
s2_m = 0.0
t_m = 0.0
owd_m = 0.0
index = 0

while (s1.readline() != "") and (s2.readline() != ""):
    s1r = s1.readline()
    s1r_ts = s1r.split(",")
    s1_m += float(s1r_ts[1])-float(s1r_ts[0])
    s2r = s2.readline()
    s2r_ts = s2r.split(",")
    s2_m += float(s2r_ts[1])-float(s2r_ts[0])
    t_m += float(s2r_ts[1]) - float(s1r_ts[0])
    owd_m += (float(s2r_ts[1]) - float(s1r_ts[0])) - (float(s1r_ts[1])-float(s1r_ts[0])) - (float(s2r_ts[1])-float(s2r_ts[0]))
    index += 1


s1_m = s1_m/float(index)
print "ts1 medio = "+ str(s1_m) + " micros"

s2_m = s2_m/float(index)
print "ts2 medio = "+ str(s2_m) + " micros"

t_m = t_m/float(index)
print "t medio = "+ str(t_m) + " micros"

owd_m = owd_m/float(index)
print "owd medio = "+ str(owd_m) + " micros"


s1.close();
s2.close();
