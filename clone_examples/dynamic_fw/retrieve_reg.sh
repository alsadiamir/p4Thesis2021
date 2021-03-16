#!/bin/bash
simple_switch_CLI --thrift-port=9090 < read_flag.txt | grep flag | cut -d ' ' -f 3
