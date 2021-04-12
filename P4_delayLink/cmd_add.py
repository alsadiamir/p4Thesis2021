import os
import optparse

parser = optparse.OptionParser()
parser.add_option('-f', '--file', action = "store", dest = "file", help="file for cmd add", default = "cmd.txt" )

options, args = parser.parse_args()

os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9090 < s1-commands.txt')
os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9091 < s2-commands.txt')
os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9092 < s3-commands.txt')
os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9093 < s4-commands.txt')
