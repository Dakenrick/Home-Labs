# Home-Labs

This repository contains networking lab configurations, automation tools, and backup scripts for Cisco CCNP study labs and other networking technologies.

## Project Structure

```
CCNP-Labs/
├── EVE-NG/                # Lab environments
│   ├── CCNP-FHRP-LABS/
│   ├── CCNP-SDWAN-LABS/
│   └── CCNP-PING-SNMP-SYSLOG-LABS/
├── ansible/              # Ansible playbooks and inventory
└── network_backup.py     # Python backup script
```

## Network Configuration Backup

You can backup network device configurations using either Python or Ansible.

### Using Python Script

1. Install required packages:
```bash
pip install netmiko pyyaml
```

2. Run the backup script:
```bash
# Backup all lab configurations
python CCNP-Labs/network_backup.py

# View logs in network_backup.log
```

The script will:
- Automatically detect lab types
- Use appropriate commands for each lab type
- Save backups in respective lab directories
- Create detailed logs

### Using Ansible Playbook

1. Install required collections:
```bash
ansible-galaxy collection install cisco.ios
```

2. Run the backup playbook:
```bash
# Backup all labs
cd CCNP-Labs/ansible
ansible-playbook -i inventory backup.yml

# Backup specific lab type
ansible-playbook -i inventory backup.yml --limit ccnp_sdwan
ansible-playbook -i inventory backup.yml --limit ccnp_fhrp
ansible-playbook -i inventory backup.yml --limit ccnp_ping_snmp_syslog
```

### Backup Locations

Backups are organized by lab type:
- SDWAN: `CCNP-Labs/EVE-NG/CCNP-SDWAN-LABS/Backups/`
- FHRP: `CCNP-Labs/EVE-NG/CCNP-FHRP-LABS/Backups/`
- PING-SNMP-SYSLOG: `CCNP-Labs/EVE-NG/CCNP-PING-SNMP-SYSLOG-LABS/Backups/`

### Lab-Specific Commands

Each lab type has customized backup commands:

#### SDWAN Labs
- show sdwan running-config
- show sdwan control connections
- show system status

#### FHRP Labs
- show running-config
- show vrrp brief
- show hsrp brief
- show glbp brief
- show track

#### PING-SNMP-SYSLOG Labs
- show running-config
- show logging
- show snmp
- show snmp user
- show snmp group

## Adding New Lab Types

1. Update `backup_config.yml` with new device groups
2. Add lab-specific commands in `network_backup.py`
3. Update Ansible inventory with new device groups

## Troubleshooting

Common issues and solutions:
- SSH connection failures: Verify device SSH enabled and reachable
- Authentication errors: Check username/password in config
- Backup failures: Check directory permissions and device access
