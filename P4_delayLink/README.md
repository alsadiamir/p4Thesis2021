# OWD delay link
A 2 hosts, 4 switch network that calculates OWD using a probe based algorithm.
<img src="/misc/img/P4img-Test_delayLink.png" alt="dl.png" style="height=70%"/> 

## How to calculate OWD
Every test file is formatted as follows:

timestamp ingress switch 1 first time, timestamp egress switch 1 first time, timestamp ingress switch 2, timestamp egress switch 2, timestamp ingress switch 1 second time, timestamp egress switch 1 second time.

## RTT and OWD
The RTT between 2 switches is calculated with the help of a probe. The probe goes through s1-s2 and s1 again. This choice is due to the fact that it is always better to use the same clock to measure a delay. 

In figure, the RTT is equals to the sum of the **red** and **purple** paths. It is equals to: **timestamp egress switch 1 second time - timestamp ingress switch 1 first time**.

Then, the OWD is obtained by subtracting the **red** path from the RTT and by halving the result. We simply calculate a bunch of values to start with.

**RS1(time spent in the first switch) = (timestamp egress switch 1 first time - timestamp ingress switch 1 first time) + (timestamp egress switch 1 second time - timestamp ingress switch 1 second time)**

**RS2(time spent in the second switch) = timestamp egress switch 2 - timestamp ingress switch 2**

**OWD = ( RTT - (RS1 + RS2) ) / 2**

## Test results
Every test is simulated through the use of **linux traffic control (tc)** with the help of a simulated Mininet network. The test results are divided in 2 cases: normal and good case.
The error is the **relative error** and is calculated as follows: 

__RE =( (average value of delay measured - delay)/delay ) x 100__
|   **delay(ms)**|                         **Normal case**                         |                         **Good case**                         |  
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| 10 | 5.22% | 1.70% | 
| 50 | 6.38% | 0.31% | 
| 100 | 5.75% | 0.53% | 
| 200 | 0.36% | 0.31% | 

## How to run a test
First, set the Mininet delay value. 
1 - Go on the file test_topo.py and edit it.
2 - Go on line 45 and edit the value of delay in the line **self.addLink(switch2, switch3, port1=3,port2=3, delay="200ms")** - format are Xms, Xs, etc.. with X being the value of the delay

Then, open 2 terminals in P4_delayLink/.

### Collecting data
In the **first terminal** run the following commands, to:
1. generate a JSON file with the description of the basic.p4 rules
2. start the topography described in test_topo.py
3. open a terminal for every node - we will call them h1 and h4
```shell
p4c-bm2-ss --p4v 16 basic.p4 -o basic.json
sudo python start_test_topo.py
xterm h1 h4
```

In the **second terminal** run the following commands, to install rules into the switches:
```shell
sudo python cmd_add.py
```

Then, in the **h4 terminal**, run the following command to start listening to TCP packets - you need to specify the file in which you want to save tests (-f option, csv file preferred)
```shell
./receive.py -f filename.csv
```

Then, in the **h1 terminal**, run the following command to send 5 packets:
```shell
./sendT.sh
```

### Calculating the OWD
Run the following to calculate OWD, you will see RS1 and RS2 calculation, as well as RTT - you need to specify the file from which you want to calculate OWD (-f option, format specified above):
```shell
./calculate_OWD.py -f filename
```
