# Many data loops
A 2 hosts, 2 switch network that calculates OWD using a Many-data-loops method.
<img src="/misc/img/P4img-test_MDL.png" alt="cll.png" style="zoom:30%;"/> 

# How is the algorithm calculated
First, the RTT between h1 and h2 is calculated. This is the RTT of a packet that goes through **controller - (s1 - s2 - s1 - s2 - ... for ever)**.
The packet carries the timestamp at the time the packet is sent and the number of switch it passed through (we will call it **N**). Everytime it passes through a 
switch the queuing delay is subtracted from the timestamp. When the number of switch is equals to a fixed dimension (100 by default) the packet is cloned to the controller,
that calculates the RTT as follows:

**rtt_t = current time - timestamp of the packet - sum of queuing delays om each switch**

The final OWD is:
**OWD = rtt_t / 2**


# How to obtain the data
First open 2 terminals in test_algorithms/Many_Data_Loops.

In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the basic.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1 and h2
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h2 
```

In the **second terminal** run the following command to add the rules written in s1.txt to the switch s1, that enables rtt_t flow:
```shell
sudo python cmd_add.py
```
# RTT_T

Then, in the **h3 terminal**, run the following command to start listening to TCP packets:
```shell
./receive.py
```

Then, in the **h1 terminal**, run the following command to send the probe:
```shell
./send_probe.py
```

**If the file data.csv is generated and has 50 entries the action was performed correctly**

# OWD

In the **second terminal** run the following to calculate the final OWD given **THE ENTRIES previously calculated**
```shell
sudo python calculate_OWD.py
```

