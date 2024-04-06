from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
import time
import datetime

CCNP_CRTL = ['192.168.100.24', '192.168.100.25', '192.168.100.26', '192.168.100.39', '192.168.100.40', '192.168.100.41']
CCNP_SDWAN = ['192.168.100.20', '192.168.100.27', '192.168.100.36', '192.168.100.37', '192.168.100.38', '192.168.100.42']
CCNP_EDGES = ['192.168.100.28', '192.168.100.30', '192.168.100.33']

TYPE_XR = 'cisco_xr'
TYPE_XE = 'cisco_xe'
TYPE_EOS = 'arista_eos'

home_dir = '/home/dakenrick/Documents/Home-Labs/CCNP-Labs/EVE-NG/CCNP-SDWAN-LABS/Backups/'

# Run against IP list for IOS_XR devices.
def BACKUP(TYPE, IP_LIST, USERNAME, PASSWORD):
    TNOW = datetime.datetime.now().replace(microsecond=0)
    for IP in IP_LIST:
        DEVICE = {
            'device_type': TYPE,
            'ip': IP,
            'username': USERNAME,
            'password': PASSWORD
        }
        print('\n ### Connecting to ' + IP + ' ' + str(TNOW) + '### \n')
        try:
            net_connect = ConnectHandler(**DEVICE)
            net_connect.enable()
        
        except AuthenticationException:
            print('Authentication Failure.')
            continue

        except SSHException:
            print('Make sure SSH is enabled.')
            continue
        
        print('Starting config backup ' + str(TNOW))
        output = net_connect.send_command('show sdwan run', read_timeout=300)
        SAVE_FILE = open(home_dir + 'CCNP_SDWAN_' + IP + '.ios', 'w')
        SAVE_FILE.write(output)
        SAVE_FILE.close
        print('\n Finished backing up config \n')

#BACKUP(TYPE_XE, CCNP_SDWAN, 'cisco', 'Cisco123')
BACKUP(TYPE_XE, CCNP_EDGES, 'admin', 'Cisco12345')
#BACKUP(TYPE_XE, CCNP_CRTL, 'admin', 'Cisco123')