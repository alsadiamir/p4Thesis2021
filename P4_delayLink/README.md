## OWD delay link
A 2 hosts, 4 switch network that calculates OWD using a probe based algorithm.
<img src="/misc/img/P4img-Test_delayLink.png" alt="dl.png" style="height=70%"/> 

## How to calculate OWD
Every test file is formatted as follows:

timestamp ingress switch 1 first time, timestamp egress switch 1 first time, timestamp ingress switch 2, timestamp egress switch 2, timestamp ingress switch 1 second time, timestamp egress switch 1 second time.

### First, the RTT
The RTT between 2 switches is calculated with the help of a probe. The probe goes through s1-s2 and s1 again. This choice is due to the fact that it is always better to use the same clock to measure a delay. 

In figure, the RTT is equals to the sum of the **red** and **purple** paths. It is equals to: **timestamp egress switch 1 second time - timestamp ingress switch 1 first time**.

Then, the OWD is obtained by subtracting the **red** path from the RTT and by halving the result. We simply calculate a bunch of values to start with.

**RS1(time spent in the first switch) = (timestamp egress switch 1 first time - timestamp ingress switch 1 first time) + (timestamp egress switch 1 second time - timestamp ingress switch 1 second time)**

**RS2(time spent in the second switch) = timestamp egress switch 2 - timestamp ingress switch 2**

**OWD = RTT - (RS1 + RS2)**

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

