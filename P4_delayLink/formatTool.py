f = open("data.csv","r")
w = open("data_final.csv","w") 
x = f.readline()
test = x.split(",")
counter = 0
delay = 1
counter2 = 0
for line in test:
	counter = counter + 1
	w.write(line + ",")
	if(counter == 4):
		counter2 = counter2 + 1
		w.write(str(delay) + ",")
		w.write("\n")
		counter = 0
		if(counter2 == 4):
			delay = delay + 1
			counter2 = 0

f.close();
w.close();
