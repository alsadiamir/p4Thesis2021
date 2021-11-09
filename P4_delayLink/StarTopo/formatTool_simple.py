f = open("data.csv","r")
w = open("data_final.csv","w") 
x = f.readline()
test = x.split(",")
counter = 0
for line in test:
	counter = counter + 1
	w.write(line + ",")
	if(counter == 4):
		w.write("10" + ",")
		w.write("\n")
		counter = 0
f.close();
w.close();
