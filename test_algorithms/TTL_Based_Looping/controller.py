import subprocess
import os

last_val = 0
register_val = 0
while 1:
    if(last_val != register_val):
        print 'im here'
        if(register_val == 1):
            last_val = register_val
            os.system('sudo python cmd_add.py -f rule.txt')
        if(register_val == 2):
            last_val = register_val
            print 'action happened!!!'
    else:
        register_val = subprocess.check_output('sudo ./retrieve_reg.sh', shell=True).strip()
        register_val = int(register_val)
        print register_val
