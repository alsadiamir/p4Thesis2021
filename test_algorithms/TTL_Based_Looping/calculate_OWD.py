t = open("data_millisecs.csv","r")
tr = t.readline()
t_lines = tr.split(",")


rtt_m = 0.0
index = 0
for line in t_lines:
    if line != "":
        rtt_m += float(line)
        index += 1

rtt_m = rtt_m/float(index)

print "OWD = " +str(rtt_m) + " micros"

#print "OWD = " +str(float(rtt_m/2)) + " micros"

t.close();
