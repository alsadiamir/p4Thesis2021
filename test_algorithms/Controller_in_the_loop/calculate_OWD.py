t = open("data_TS.csv","r")
s1 = open("data_S1.csv","r")
s2 = open("data_S2.csv","r")
tr = t.readline()
s1r = s1.readline()
s2r = s2.readline()
t_lines = tr.split(",")
s1r_lines = s1r.split(",")
s2r_lines = s2r.split(",")

t_m = 0.0
index = 0
for line in t_lines:
    if line != "":
        t_m += float(line)
        index += 1

t_m = t_m/float(index)
print "ts medio = "+ str(t_m)

s1_m = 0.0
index = 0
for line in s1r_lines:
    if line != "":
        s1_m += float(line)
        index += 1

s1_m = s1_m/float(index)
print "ts1 medio = "+ str(s1_m)

s2_m = 0.0
index = 0
for line in s2r_lines:
    if line != "":
        s2_m += float(line)
        index += 1

s2_m = s2_m/float(index)
print "ts2 medio = "+ str(s2_m)

rtt = float(t_m - ((s1_m + s2_m) / 2))

print "ts = " +str(rtt) + " micros"

print "OWD = " +str(float(rtt/2)) + " micros"

t.close();
s1.close();
s2.close();
