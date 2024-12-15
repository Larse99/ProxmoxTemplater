# ProxmoxTemplater
This project creates Cloud-init enabled images for Proxmox. This enables the user to use the cloudinit section in Proxmox and let them configure the VM before it started. This projects also enables it to use custom CloudInit configurations while building VMs.

Please check the included settings.yaml and cloudConfigs/ubuntu.yaml for examples.

_This is stil in beta_

## New in this version
Added support for custom VM settings:
- Cores
- Memory
- Networking Device
- Networking VLAN tags
- Enable/Disable Guest agent

Renamed the valuenames for the settings.yaml
Bugfixes

## To-do:
More customizations :-DDDDDD
Documentation for classes. This version introduced some additions who needs to be documented.