# Controller in the loop
A 4 hosts, 2 switch network that calculates OWD using a Controller-in-the-Loop method.
<img src="/misc/img/P4img-test_CLL.png" alt="cll.png" style="zoom:30%;"/> 

# How is the algorithm calculated
First, the RTT between h1 and h3 is calculated: the message sent carries the timestamp before being sent (by the controller) and the RTT is calculated as 

# How to run it
First open 2 terminals in clone_example/basic.

In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the basic.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1, h2 and h3 
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h2 h3
```

In the **second terminal** run the following command to add the rules written in cmd.txt to the switch s1, that enable forwarding between h1 and h2 with the clone to h3:
```shell
sudo python cmd_add.py
```

Then, in the **h2 and h3 terminals**, run the following command to start listening to TCP packets:
```shell
./receive.py
```

Then, in the **h1 terminal** run the following command to send a packet to h2:
```shell
./send.py 10.0.0.2 "message payload"
```

**If h3 receives the message then the clone was successfully performed**
