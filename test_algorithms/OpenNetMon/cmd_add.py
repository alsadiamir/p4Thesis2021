import os
import optparse

parser = optparse.OptionParser()
parser.add_option('-f', '--file', action = "store", dest = "file", help="file for cmd add", default = "cmd.txt" )

options, args = parser.parse_args()

#os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9090 < ' + options.file)
#os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9091 < ' + options.file)

os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9090 < s1.txt')
os.system('sudo /home/vagrant/behavioral-model/targets/simple_switch/simple_switch_CLI --thrift-port=9091 < s2.txt')
