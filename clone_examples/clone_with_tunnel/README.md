# Ingress 2 egress cloning and packet tunneling
A 4 hosts, 2 switch network that clones every packet exchanged between h1 and h2 to h3 with the help of a tunneling rule. Packets exchanged between h3 and h4 are tunneled to h3 as well.
<img src="../../misc/img/P4img-basic_with_tunnel.png" alt="tunnel.png" style="zoom:30%;"/> 

**Host IPs are numbered from 10.0.0.1 to 10.0.0.4 from h1 to h4.**

# How to run it
**FIRST STEP**

First open 2 terminals in clone_example/clone_with_tunnel.

In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the clone_with_tunnel.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1, h2, h3 and h4
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h2 h3 h4
```

In the **second terminal** run the following command to:
1. Add the rules written in cmd.txt to the switch s1, to enable forwarding between h1 and h2, with the clone to h3.
2. Add the rules written in cmd2.txt to the switch s2, to tunnel packets coming from h4 and h3 to h3.
```shell
sudo python cmd_add.py
```

Then, in the **h2, h3 and h4 terminals**, run the following command to start listening to TCP packets:
```shell
./receive.py
```

Then, in the **h1 terminal** run the following command to send a packet to h2:
```shell
./send.py 10.0.0.2 "message payload"
```

**If h3 receives the message then the clone was successfully performed**

**SECOND STEP**

In the **first terminal** run the following commands to open a new h3 terminal - we will call it h3(2):
```shell
xterm h3
```

Then, in the **h3(2) terminal**, run the following command to start listening to TCP packets:
```shell
./receive.py
```

Then, in the **h3 terminal** run the following command to send a packet to h4:
```shell
./send.py 10.0.0.4 "message payload"
```

**If h3(2) receives the message but not h4 then the tunnel was successfully built**
