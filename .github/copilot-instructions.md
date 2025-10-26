# AI Assistant Instructions

This repository contains networking labs, configurations, and automation tools focused on Cisco networking technologies (CCNP, SD-WAN) and network automation.

## Project Structure

- `CCNP-Labs/`: Contains Cisco CCNP study lab configurations and scripts
  - Key lab categories: FHRP, PING-SNMP-SYSLOG, SDWAN
  - Backup configurations in `Backups/` directories
- `Network_Automation/`: Python scripts and tools for network automation
  - SD-WAN REST API examples and tools
  - Network configuration backup scripts
  - Ansible playbooks for network automation

## Key Patterns and Conventions

### Network Device Backup
When working with backup scripts:
- Use the `netmiko` library for device connections
- Store device credentials as parameters (username/password)
- Group devices by type (XE, XR, EOS) and function (SDWAN, EDGES, CTRL)
- Save backups to type-specific directories with format: `LABTYPE_DEVICETYPE_IP.ios`

Example from `backup_config_cisco_arista_devices_function.py`:
```python
BACKUP(TYPE_XE, CCNP_EDGES, 'admin', 'password')  # For edge devices
```

### SD-WAN Automation
For SD-WAN API interactions:
- Use environment variables for credentials:
  - SDWAN_IP
  - SDWAN_USERNAME 
  - SDWAN_PASSWORD
- REST API class provides standard methods for API operations
- CLI commands use Click framework for parameter handling

## Critical Workflows

### Setting up a new lab
1. Create appropriate directory structure under CCNP-Labs
2. Configure devices following lab topology
3. Use backup scripts to preserve configurations

### Working with SD-WAN
1. Set environment variables for vManage access
2. Use provided CLI tools for common operations:
   - `device_list`: View fabric devices
   - `template_list`: View available templates
   - `attach/detach`: Manage device templates

## Integration Points

- Network devices: Access via SSH (port 22)
- vManage: REST API access (port 8443)
- Authentication: Local credentials or environment variables
- Configuration backup location: Local filesystem in lab-specific directories

## Common Troubleshooting

- SSH connection issues: Verify device SSH enabled
- API access failures: Check environment variables
- Backup failures: Verify directory permissions and device access