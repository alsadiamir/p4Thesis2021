#!/bin/bash
for i in {0..4}
do
  sudo ./send.py --dst_id 2 --delay 0.03 10.0.1.1 'ping'
  sleep 0.5
done
