
# Proxmox Templater

Easily convert your favorite Linux Cloud image (QCOW, .img) into a fully functional Proxmox template, ready for customization with Cloud-Init. This tool enables Cloud-Init options in Proxmox, allowing you to configure essential settings like networking from the very first boot!

## Prerequisites

Before using this tool, ensure you have **Python 3.11** installed. While newer versions may work, this script has been tested specifically with Python 3.11.

## Installation

Installation is straightforward. Since this tool is available as a Python package, you can install it using `pip`. If you prefer a clean setup, you can run it within a virtual environment—this is my recommended approach.

### Quick Installation

```
# Clone the repository
git clone https://github.com/Larse99/ProxmoxTemplater.git

# Set up a Python virtual environment (optional but recommended)
cd ProxmoxTemplater && python3 -m venv venv && source venv/bin/activate

# Install the package
python3 -m pip install -e .

# Run the tool
ptemplater -c <settings.yaml>
```

## Usage

Using this tool is simple. You'll need:

1.  A `settings.yaml` file (an example is provided in the `Example` directory).
2.  A Linux Cloud image (e.g., Debian, Ubuntu, AlmaLinux).
3.  A Cloud-Init configuration file (also available in the `Example` directory).
    

### How It Works

The script reads the contents of the `settings.yaml` file and executes its instructions. You can create multiple settings files (e.g., `ubuntu24.yaml`, `ubuntu2204.yaml`) for different templates.

After installation, you can organize your files in any way you prefer. A recommended structure looks like this:

```
|-- cloudConfigs
|   |-- ssh.key
|   |-- almalinux9.yaml
|   |-- debian12.yaml
|   `-- ubuntu2404.yaml
|-- Templates
|   |-- alma9-settings.yaml
|   |-- debian12-settings.yaml
|   `-- ubuntu2404-settings.yaml
|-- cloudImages
|   |-- almalinux-9.5-amd64.qcow2
|   |-- debian-12.qcow2
|   |-- jammy-server-cloudimg-amd64.img
|   `-- noble-server-cloudimg-amd64.img
```

### Example Usage

The example below is based on the structure above. Check out the examples below to get started :) 

#### settings.yaml

```
# Proxmox template settings - customize your VM as needed
global_settings:
  qm_bin: "/usr/sbin/qm"
  
template_settings:
  # VM configuration
  vm_id: "9002"
  vm_name: "Ubuntu-2204-Jammy"
  vm_inject: "cloudConfigs/settings.yaml"
  vm_image: "cloudImages/jammy-server-cloudimg-amd64.img"
  vm_size: "10G"
  vm_user: "root"
  vm_user_ssh_key: "ssh.key"
  vm_bridge: "vmbr1"
  vm_tag: "30"
  vm_cores: "2"
  vm_memory: "1024"
  vm_agent: "1"

  # Proxmox storage settings
  storage_pool: "local"
```

#### cloudConfigs.yaml

```
#cloud-config
# Full list of options: https://cloudinit.readthedocs.io/en/latest/reference/examples.html

# User management
users:
  - name: ansible
    gecos: Ansible User
    groups: wheel
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: true
    ssh_authorized_keys:
      - "ecdsa ..."

# Run commands on first boot
runcmd:
  - [ sh, -c, "echo 'Executing startup commands...'" ]
  - reboot

# Install base packages
package_update: true
packages:
  - qemu-guest-agent
  - pwgen
  - curl
  - htop
  - vim
  - net-tools
  - lldpad
  - ncdu
  - git
  - btop
```

### cloudImages Directory Example

```
|-- cloudImages
|   |-- almalinux-9.5-amd64.qcow2
|   |-- debian-12.qcow2
|   |-- jammy-server-cloudimg-amd64.img
|   `-- noble-server-cloudimg-amd64.img
```

## License

This project is licensed under the **MIT License**. Feel free to use, modify, and share it as you like!

