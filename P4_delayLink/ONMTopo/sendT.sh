#!/bin/bash
for i in {0..4}
do
  sudo python2 send.py --dst_id 1 10.0.1.2 'ping'
  sleep 0.5
done
