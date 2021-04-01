# TTL based looping
A 2 hosts, 2 switch network that calculates OWD using a TTL-based-looping method.
<img src="/misc/img/P4img-test_TTL.png" alt="ttl.png" style="zoom:30%;"/> 

# How is the algorithm calculated
First, the RTT between h1 and h2 is calculated. This is the RTT of a packet that goes through **controller - (s1 - s2 - s1 - s2 - ... for TTL times - default TTL is 100)**.
The packet carries the timestamp at the time the packet is sent. Everytime it passes through a switch the TTL decreases. 
When the TTL reaches 0, it is cloned to the controller that calculates the OWD as follows:

**OWD = current time - timestamp of the packet / TTL(number of iterations)**

# How to obtain the data
First open 2 terminals in test_algorithms/TTL_Based_Looping.

In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the basic.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1, h2 and h3
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h2 h3
```

In the **second terminal** run the following command to add the rules written in s1.txt to the switch s1, that enables rtt_t flow:
```shell
sudo python cmd_add.py
```
# OWD of every packet

Then, in the **h2 and h3 terminal**, run the following command to start listening to TCP packets:
```shell
./receive.py
```

Then, in the **h1 terminal**, run the following command to send 50 packets:
```shell
./sendT.sh
```

**If the file data_milliseconds.csv is generated and has 50 entries the action was performed correctly**

# OWD

In the **second terminal** run the following to calculate the final OWD given **THE ENTRIES previously calculated**. It calculates the average OWD.
```shell
sudo python calculate_OWD.py
```

