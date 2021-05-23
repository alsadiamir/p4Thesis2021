# How to run it

First open a terminal under the folder:  ngsdn-tutorial/ 

In this folder, run the following commands, to:
1. start ONOS and Mininet (4 switches, 2 hosts topo)
2. build and install the ngsdn-tutorial app
3. install the json description of the Mininet topo to ONOS
4. reload the app
```shell
make start-test-topo
make app-build app-reload
make netcfg-test-topo
make app-reload
```
Then, connect to http://localhost:8181/ to login to the app: credentials onos,rocks
**Repeat step 5 one more time if you don't see the topology after logging in**

Then, open a terminal under the folder:  uiext/ 

In this folder, run the following commands, to:
1. build and install the uiext app
2. reload the app (optional)
```shell
make app-build app-reload
make app-reload
```
Then, connect to http://localhost:8181/ and click on the upper left drop-down panel and click the section "Show OWD for path Spine1-Spine2"
You can now see the average delay measured (you can both re-fetch it or erase the measurement)
**Repeat step 3 one more time if something wen wrong in the UI**

## How to measure the OWD
Open a terminal under the folder:  ngsdn-tutorial/ 

Run the following commands, to calculate the OWD between spine 1 and spine 2:
```shell
util/mn-cmd h4 /mininet/send.py --dst_id 2 "10.0.1.1" "ping"
```

After this, you can re-fetch the OWD from the GUI.
