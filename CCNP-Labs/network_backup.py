#!/usr/bin/env python3

import os
import sys
import logging
import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException, SSHException
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_backup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class NetworkBackup:
    # Device types
    TYPE_XR = 'cisco_xr'
    TYPE_XE = 'cisco_xe'
    TYPE_EOS = 'arista_eos'
    TYPE_NX = 'cisco_nxos'
    TYPE_ASA = 'cisco_asa'
    
    # Lab types and their default commands
    LAB_TYPES = {
        'CCNP-SDWAN': {
            'commands': [
                'show sdwan running-config',
                'show sdwan control connections',
                'show system status'
            ]
        },
        'CCNP-FHRP': {
            'commands': [
                'show running-config',
                'show vrrp brief',
                'show hsrp brief',
                'show glbp brief',
                'show track'
            ]
        },
        'CCNP-PING-SNMP-SYSLOG': {
            'commands': [
                'show running-config',
                'show logging',
                'show snmp',
                'show snmp user',
                'show snmp group'
            ]
        }
    }

    def __init__(self, config_file='backup_config.yml'):
        """Initialize with configuration file"""
        self.config = self._load_config(config_file)
        self.backup_dir = Path(self.config.get('backup_dir', 'backups'))
        self.backup_dir.mkdir(exist_ok=True)

    def _load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return {
                'backup_dir': 'backups',
                'device_groups': {
                    'CCNP_CRTL': {
                        'type': 'cisco_xe',
                        'devices': ['192.168.100.24', '192.168.100.25', '192.168.100.26'],
                        'username': 'admin',
                        'password': 'Cisco123'
                    },
                    'CCNP_SDWAN': {
                        'type': 'cisco_xe',
                        'devices': ['192.168.100.20', '192.168.100.27'],
                        'username': 'admin',
                        'password': 'Cisco123'
                    }
                }
            }

    def backup_device(self, device_ip, device_type, username, password, commands=None):
        """Backup a single device's configuration"""
        if commands is None:
            commands = ['show running-config']

        device = {
            'device_type': device_type,
            'ip': device_ip,
            'username': username,
            'password': password
        }

        try:
            logger.info(f"Connecting to {device_ip}")
            with ConnectHandler(**device) as net_connect:
                net_connect.enable()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                device_dir = self.backup_dir / device_type
                device_dir.mkdir(exist_ok=True)
                
                for command in commands:
                    output = net_connect.send_command(command, read_timeout=300)
                    filename = f"{device_ip}_{command.replace(' ', '_')}_{timestamp}.txt"
                    backup_path = device_dir / filename
                    
                    with open(backup_path, 'w') as f:
                        f.write(output)
                    logger.info(f"Saved {command} output to {backup_path}")

                return True

        except AuthenticationException:
            logger.error(f"Authentication failed for {device_ip}")
        except SSHException:
            logger.error(f"SSH connection failed for {device_ip}. Check if SSH is enabled.")
        except Exception as e:
            logger.error(f"Error backing up {device_ip}: {str(e)}")
        
        return False

    def backup_group(self, group_name):
        """Backup all devices in a group"""
        if group_name not in self.config['device_groups']:
            logger.error(f"Group {group_name} not found in configuration")
            return False

        group = self.config['device_groups'][group_name]
        success = True

        for device_ip in group['devices']:
            if not self.backup_device(
                device_ip,
                group['type'],
                group['username'],
                group['password'],
                group.get('commands')
            ):
                success = False

        return success

    def backup_all(self):
        """Backup all configured device groups"""
        success = True
        for group_name in self.config['device_groups']:
            if not self.backup_group(group_name):
                success = False
        return success

def main():
    backup = NetworkBackup()
    if backup.backup_all():
        logger.info("All backups completed successfully")
    else:
        logger.warning("Some backups failed - check the logs for details")

if __name__ == "__main__":
    main()