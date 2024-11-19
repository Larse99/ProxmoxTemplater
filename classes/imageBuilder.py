# This class builds the actual Virtual Machine from the template
import os
import sys
import shutil
import subprocess

class imageBuilderError(Exception):
    """Custom exception for ImageBuilder errors."""

class imageBuilder:
    """
        This class builds the VM, and the final template/image in Proxmox.

        - _runCommand:
          This method is used to run a command using subprocess.
          The method is protected, because we don't want it to be used from somewhere else than this class.

        - _vmExists:
          Checks if a VM with the desired vmid already exists. Returns True if it exists, returns False if it doesn't exist.

        - _vmDestroy:
          Destorys a Virtual Machine (delete).

        - _resizeImage:
          Resizes a Linux disk image to the desired size.

        - _createTemporaryVM:
          Creates a temporary VM. To create a Template, we first have to create a VM which we inject with all the necessary settings

        - _importDisk:
          Imports the new disk to the VM. This will also take care of the storagepool used.

        - _setupcloudInit:
          Sets up CloudInit. Injects the VM with the right settings and runs the base Proxmox settings/commands like setting root SSH keys,
          This method also adds the CloudInit disk, so the booting VM will use the settngs.

        - _changeBootOrder;
          By default the VM will boot from disk first, except if stated otherwise. This method takes care of the bootorder, so the VM boots
          from a CloudImage and uses its disk drive for CloudInit.

        - convertVMTemplate:
          Just converts the VM to a template, so you can clone and make changes in Proxmox.

        - CreateVM:
          This is the main method of this class. This runs all the methods mentioned above and takes care of the creation of a CloudInit enabled image.

        - returnValue:
          This is just used for troubleshooting or looking at how the class intepretates the method.

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

    def _vmDestroy(self):
        """ Destroys existing VM, if any exists """
        if self._vmExists():
            print(f"WARNING: VMID {self.vmid} already exists")
            self._runCommand(f"{self.qmBin} destroy {self.vmid}")

    def _resizeImage(self):
        """ Resizes the CloudImage to the desired size """
        print(f"INFO: Resizing image")
        self._runCommand(f"qemu-img resize --shrink {self.linuxImage} {self.imageSize}")

    def _createTemporaryVM(self):
        """ Creates a temporary VM, we can interact with it """
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

    def _importDisk(self):
        """ Imports the disk to the VM """
        self._runCommand(f"{self.qmBin} importdisk {self.vmid} {self.linuxImage} {self.storagePool}")

    def _setupCloudInit(self):
        """ Sets up Cloud Init """
        print(f"INFO: Setting up CloudInit")

        # Copy ciFile to desired storage (Local)
        try:
            destination = os.path.join("/var/lib/vz/snippets", os.path.basename(self.ciFile))
            shutil.copy2(self.ciFile, destination)
        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            raise

        # Add Cloud-Init disk
        try:
            self._runCommand(f"{self.qmBin} set {self.vmid} --scsihw virtio-scsi-pci --virtio0 {self.storagePool}:{self.vmid}/vm-{self.vmid}-disk-1.raw,discard=on")
        except imageBuilderError as e:
            print(f"ERROR: {e}")
            raise

        print(f"INFO: Injecting Base Cloud-init data")
        # Injecting Base Cloud-Init data
        ciData = [
            f'{self.qmBin} set {self.vmid} --cicustom "vendor={self.storagePool}:snippets/{os.path.basename(self.ciFile)}"',
            f"{self.qmBin} set {self.vmid} --ciuser {self.vmUser}",
            f"{self.qmBin} set {self.vmid} --sshkeys {self.sshKey}",
            f"{self.qmBin} set {self.vmid} --ipconfig0 ip=dhcp"
        ]

        # Execute each command in ciData
        for data in ciData:
            self._runCommand(data)

    def _changeBootOrder(self):
        """ Changes the boot order, so the VM doesn't try to boot from the CloudInit disk """
        print(f"INFO: Set up bootorder...")

        # Set the bootorder
        try:
            self._runCommand(f"{self.qmBin} set {self.vmid} --boot order=virtio0")
            self._runCommand(f"{self.qmBin} set {self.vmid} --ide2 {self.storagePool}:cloudinit")
        except imageBuilderError as e:
            print(f"ERROR: Failed to configure boot order or CloudInit: {e}")
            raise

    def _convertVMToTemplate(self):
        """ Converts the VM to Template """

        print(f"INFO: Converting VM to Template")
        try:
            self._runCommand(f"{self.qmBin} template {self.vmid}")
        except imageBuilderError as e:
            print(f"ERROR: Failed to convert the VM to a Template {e}")
            raise

    def createVM(self):
        """ Main method for creating the VM """
        try:
            self._vmDestroy()
            self._resizeImage()
            self._createTemporaryVM()
            self._importDisk()
            self._setupCloudInit()
            self._changeBootOrder()
            self._convertVMToTemplate()
            print(f"SUCCESS: Template created successfully!")
        except imageBuilderError as e:
            print(f"ERROR: {e}")

    # Debug
    def returnValue(self):
        output = self._runCommand("qm list")
        return output

        # return f"{self.qmBin}, {self.linuxImage}, {self.vmid}, {self.imageSize}, {self.name}, {self.ciFile}, {self.storagePool}, {self.vmUser}, {self.sshKey}, {self.debug}"

# class debuggings
img = imageBuilder("/usr/sbin/qm", "../images/noble-server-cloudimg-amd64.img", "9001", "10G", "ubuntu2404-template", "../snippets/ubuntu.yaml", "local", "root", "../ssh.key", False)

# print(img.returnValue())
# print(img._vmExists())
print(img.createVM())

#     def returnValue(self):
#         return f"{self.config}, {self.qm_bin}"
        

# # Class debuggings
# img = imageBuilder("settings.yml", "/usr/bin/qm")
# print(img.returnValue())
