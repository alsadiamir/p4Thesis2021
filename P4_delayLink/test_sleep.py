#!/usr/bin/env python
import time

starttime = time.time() * 1000
time.sleep(0.05)
endtime = time.time() * 1000
print "diff=" +str(endtime - starttime)
