# This class builds the actual Virtual Machine from the template
import os
import sys
import subprocess

class imageBuilder:
    """
        This class builds the VM, and the final template/image in Proxmox.

        - _runCommand:
          This method is used to run a command using subprocess.
          The method is protected, because we don't want it to be used from somewhere else than this class.

        - _vmExists:
          Checks if a VM with the desired vmid already exists. Returns True if it exists, returns False if it doesn't exist.

        - createVM
          This method creates the actual VM.

    """

    def __init__(self, qmBin, linuxImage, vmid, imageSize, name, ciFile, storagePool, vmUser, sshKey, debug):
        self.qmBin          = qmBin
        self.linuxImage     = linuxImage
        self.vmid           = vmid
        self.imageSize      = imageSize
        self.name           = name
        self.ciFile         = ciFile
        self.storagePool    = storagePool
        self.vmUser         = vmUser
        self.sshKey         = sshKey
        self.debug          = debug

    def _runCommand(self, cmd):
        """ Runs shell commands. Needed for the qm binary."""

        # Run the command, capture stdout and stderr separately
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Check return code
        if result.returncode != 0:
            print(f"ERROR: {result.stderr.strip()}")
            sys.exit(result.returncode)
        elif result.stderr:
            print(f"ERROR: {result.stderr.strip()}")
            sys.exit(result.returncode)

        # If everything is OK, return the output :)
        return result.stdout.strip()

    def _vmExists(self):
        """ Checks if a VM or Template already exists... """

        # Get a list of VMs
        vmList = self._runCommand(f"{self.qmBin} list").strip().split('\n')

        # Check if a VM with the vmid already exists. If so: return true, else return false.
        for line in vmList:
            if self.vmid in line.split():
                return True

        # If no match found, just return false. There is no VM with this ID.
        return False

    def createVM(self):
        """ Creates the VM and the actual template, based on the provided configuration """

        # 1. Check if VM or template already exists
        if self._vmExists() is True:
            print(f"WARNING: VMID {self.vmid} already exists")

            # VM/Template already exists. Let's remove it, so we can create a new image
            if not self._runCommand(f"{self.qmBin} destroy {self.vmid}"):
                print(f"SUCCESS: Removed old VM Template with VMID {self.vmid}")
            else:
                print(f"ERROR: Failed to remove old VM Template. Existing...")
                sys.exit(1)
        elif self._vmExists() is False:
            print(f"INFO: No VM with VMID {self.vmid} found. Continuing..")
        
        # 2. Resize image to desired size
        print(f"INFO: Resizing image")
        if self._runCommand(f"qemu-img resize --shrink {self.linuxImage} {self.imageSize}"):
            print(f"SUCCESS: Resized image to {self.imageSize}")
        else:
            print(f"ERROR: Failed to resize image")
            sys.exit(1)

        # 3. Creating the Proxmox VM
        print(f"INFO: Creating temporary Virtual Machine: {self.vmid}")
        try:
            self._runCommand(
                f""" {self.qmBin} create {self.vmid} --name {self.name} --ostype l26 \
                --memory 1024 --balloon 0 \
                --agent 1 \
                --bios ovmf --machine q35 --efidisk0 {self.storagePool}:0,pre-enrolled-keys=0 \
                --cpu host --cores 2 --numa 1 \
                --vga serial0 --serial0 socket \
                --net0 virtio,bridge=vmbr2,mtu=1
                """
            )
        except:
            print("something hapened.")

        # 4. Add disk to VM
        print(f"INFO: Importing disk...")
        if self._runCommand(f"{self.qmBin} importdisk {self.vmid} {self.linuxImage} {self.storagePool}"):
            print(f"SUCCESS: Imported the disk successfully!")
        else:
            print(f"ERROR: Something went wrong while importing the disk")
            sys.exit(1)

        # 5. Setting up CloudInit
        print(f"INFO: Setting up CloudInit")
        if self._runCommand(f"{self.qmBin} set {self.vmid} --scsihw virtio-scsi-pci --virtio0 {self.storagePool}:{self.vmid}/vm-{self.vmid}-disk-1.raw,discard=on"):
            print(f"SUCCESS: Set up CloudInit successfully!")
        else:
            print(f"ERROR: Something went wrong while setting up CloudInit.")
            sys.exit(1)
            










    # Debug
    def returnValue(self):
        output = self._runCommand("qm list")
        return output

        # return f"{self.qmBin}, {self.linuxImage}, {self.vmid}, {self.imageSize}, {self.name}, {self.ciFile}, {self.storagePool}, {self.vmUser}, {self.sshKey}, {self.debug}"



# class debuggings
img = imageBuilder("/usr/sbin/qm", "../images/noble-server-cloudimg-amd64.img", "9001", "10G", "ubuntu2404-template", "snippets/ubuntu.yaml", "VMStorage", "root", "ssh.key", False)

# print(img.returnValue())
# print(img._vmExists())
print(img.createVM())

#     def returnValue(self):
#         return f"{self.config}, {self.qm_bin}"
        

# # Class debuggings
# img = imageBuilder("settings.yml", "/usr/bin/qm")
# print(img.returnValue())