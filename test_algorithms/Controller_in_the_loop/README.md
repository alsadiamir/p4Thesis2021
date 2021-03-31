# Controller in the loop
A 4 hosts, 2 switch network that calculates OWD using a Controller-in-the-Loop method.
<img src="/misc/img/P4img-test_CLL.png" alt="cll.png" style="zoom:30%;"/> 

# How is the algorithm calculated
First, the RTT between h1 and h3 is calculated. This is the RTT of a packet that goes through **controller - s1 - s2 - controller**. It is calculated as follows: the message sent carries the timestamp before being sent (by the controller) and the RTT is:

**rtt_t = current time - timestamp of the packet**

Then, the RTT between h2 and h1 is calculated. This is the RTT of a packet that goes through **controller - s1 - controller**. It is calculated as follows: the message sent carries the timestamp before being sent (by the controller) and the RTT is:

**rtt_s1 = current time - timestamp of the packet**

Then, the RTT between h4 and h3 is calculated. This is the RTT of a packet that goes through **controller - s2 - controller**. It is calculated as follows: the message sent carries the timestamp before being sent (by the controller) and the RTT is:

**rtt_s2 = current time - timestamp of the packet**

The final OWD is:
**RTT = rtt_t - (rtt_s1 + rtt_s2) / 2**


# How to obtain the data
First open 2 terminals in test_algorithms/Controller_in_the_loop.

In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the basic.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1, h2,h3 and h4 
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h2 h3 h4
```

In the **second terminal** run the following command to add the rules written in s1.txt to the switch s1, that enable rtt_s1 and rtt_t flows:
```shell
sudo python cmd_add.py
```
# RTT_T

Then, in the **h1 terminal**, run the following command to start listening to TCP packets:
```shell
./receiveS1.py
```

Then, in the **h2 terminal**, run the following command to send 50 packets:
```shell
./sendT.sh
```

**If the file data_S1.csv is generated and has 50 entries the action was performed correctly**

# RTT_S1

Then, in the **h3 terminal**, run the following command to start listening to TCP packets:
```shell
./receiveS1.py
```

Then, in the **h1 terminal**, run the following command to send 50 packets:
```shell
./sendT.sh
```

**If the file data_TS.csv is generated and has 50 entries the action was performed correctly**

# RTT_S2

Then, in the **h3 terminal**, run the following command to start listening to TCP packets:
```shell
./receiveS2.py
```

Then, in the **h4 terminal**, run the following command to send 50 packets:
```shell
./sendT.sh
```

**If the file data_S2.csv is generated and has 50 entries the action was performed correctly**

# OWD

Run the following to calculate the final OWD given **THE ENTRIES previously calculated**
```shell
sudo python calculate_OWD.py
```

