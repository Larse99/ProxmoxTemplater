# ProxmoxTemplater
This project creates Cloud-init enabled images for Proxmox. This enables the user to use the cloudinit section in Proxmox and let them configure the VM before it started. This projects also enables it to use custom CloudInit configurations while building VMs.

Please check the included settings.yaml and cloudConfigs/ubuntu.yaml for examples.

_This is stil in beta_

## Quick how to
1. Clone the repo on your Proxmox node
2. Download a Linux cloud image e.g. for Ubuntu: https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
3. Place the Linux Cloud Image in the images directory (optionail)
4. Edit the settings.yaml to your likings, you can copy this file for different settings of course.
5. in cloudConfigs, edit the configuration to your liking. You can copy this file as well.

### Note
Be careful with the paths. Editing the files as-in, should work out of the box. If you use different settings, make sure the paths are correct.

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
