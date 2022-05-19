# ONM topology 4 hops delay link
A 2 hosts, 4 switch network that calculates OWD using a probe based algorithm.
<img src="/misc/img/publication-ONMTopo.png" alt="onm.png" style="height=70%"/> 

## How to calculate OWD
Every test file is formatted as follows:

<timestamp ingress switch 1 first time, timestamp egress switch 1 first time, timestamp ingress switch 2 first time, timestamp egress switch 2 first time, timestamp ingress switch 3 first time, timestamp egress switch 3 first time, , timestamp ingress switch 4, timestamp egress switch 4, timestamp ingress switch 3 second time, timestamp egress switch 3 second time, timestamp ingress switch 2 second time, timestamp egress switch 2 second time, timestamp ingress switch 1 second time, timestamp egress switch 1 second time>.

## RTT and OWD
The RTT between 2 switches is calculated with the help of a probe. The probe is sent from h1 and goes through s1-s2-s3-s4 and back to s3-s2-s1 to h2 which receives it. This choice is due to the fact that it is always better to use the same clock to measure a delay. 

The OWD is calculated by subtracting from the RTT the delay introduced my the switches and halving the result. 

Legend: RSij, where i=# of the switch and j=the times the packet crossed the switch.

**OWD = ( RTT - (RS11 + RS21 + RS31 + RS4 + RS32 + RS22 + RS12) ) / 2**

## Test results
Every test is simulated through the use of **linux traffic control (tc)** with the help of a simulated Mininet network. The test results are divided in 2 cases: normal and good case.
The error is the **relative error** and is calculated as follows: 

__RE =( (average value of delay measured - delay)/delay ) x 100__
|   **delay(ms)**|                         **Normal case**                         |  
| :----------------------------------------------------------: | :----------------------------------------------------------: | 
| 10 | 3.5% |
| 50 | 1.1% | 
| 100 | 0.60% | 
| 200 | 0.26% |

## How to run a test
First, set the Mininet delay value. 
1 - Go on the file test_topo.py and edit it.
2 - Go on line 43, 44 and 45 and edit the value of delay in the function **self.addLink** - format are Xms, Xs, etc.. with X being the value of the delay

Then, open 2 terminals in P4_delayLink/ONMTopo/.

### Collecting data

**(Everything is written in python2!!)**

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

Then, in the **h2 terminal**, run the following command to start listening to TCP packets - you need to specify the file in which you want to save tests (-f option, csv file preferred)
```shell
./receive.py -f filename.csv
```

Then, in the **h1 terminal**, run the following command to send 5 packets:
```shell
./sendT.sh
```

### Calculating the OWD
Run the following to calculate OWD - you need to specify the file from which you want to calculate OWD (-f option, format specified above):
```shell
./calculate_OWD.py -f filename
```

### Setting different levels of traffic using hping3 
In a **h1 terminal**, run this (number is variable from 1 to 10000 and it is the number of microseconds between packet transmission)
```shell```
hping3 -0 -i u$(number) 10.0.4.4
```
