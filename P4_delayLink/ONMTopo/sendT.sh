#!/bin/bash
for i in {0..49}
do
  sudo python2 send.py --dst_id 1 10.0.4.4 'ping'
  sleep 0.5
done
