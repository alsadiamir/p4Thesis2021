import os

os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9090 < cmd.txt')
os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9091 < cmd2.txt')
