#!/bin/bash
for i in {0..4}
do
  ./send.py --dst_id 2 10.0.1.1 'ping'
  sleep 0.5
done
