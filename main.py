# Proxmox and Cloud-Init template builder
# Version: V2.0.0
# Author: Lars Eissink

import sys
from colorama import Fore, Style

from includes.classes.configReader import readYaml
from includes.classes.argumentParser import argumentParser
from includes.classes.imageBuilder import imageBuilder
from includes.classes.welcomeMessage import welcomeMessage

from includes.functions.helpers import createDirectory, checkFileExists

# Main function
def main():
    # Initialize welcomeMessage.
    # Decided to add the information here, for ease of access
    welcome = welcomeMessage(
        title="ProxmoxTemplater",
        version="v2.1",
        author="Lars Eissink / Larse99",
        year=2024,
        github="https://github.com/Larse99/ProxmoxTemplater/",
        message="Thanks for using the ProxmoxTemplater! Let's build some amazing images :)"
    )

    welcome.display()

    print(f"\n[{Fore.YELLOW}WARNING{Style.RESET_ALL}] This script doesn't factcheck your settings yaml configuration. Make sure everything has been setup correctly!")
    print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Initializing...")

    # Initiate argumentParser
    getArguments = argumentParser()
    cliArguments = getArguments.parse()

    # Get Settings from YAML, based on user input
    getSettings = readYaml(cliArguments['config'])

    # --- Run prerequisites checks ---
    print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Running prerequisites check")

    # Check if settings exist and are valid
    if not getSettings.getGlobalSettings() and not getSettings.getTemplateSettings():
        print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] Error while reading the Settings from file: {cliArguments['config']}")
        sys.exit(1)
    else:
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] Settings")

    # Get the Global and Template settings from settings file
    globalSettings = getSettings.getGlobalSettings()
    templateSettings = getSettings.getTemplateSettings()

    # Check if necessary files exist
    # Create a list of all the files
    fileList = [
        globalSettings.get("qm_bin"),
        templateSettings.get("vm_image"),
        templateSettings.get("vm_inject"),
        templateSettings.get("vm_user_ssh_key")
    ]

    # Iterate over the list of files.
    for file in fileList:
        if not checkFileExists(file):
            print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] {file}")
            print("Exiting...")
            sys.exit(1)

        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {file}")

    # Create needed directories for cloud-init / Proxmox
    directoryList = [
        "/var/lib/vz/snippets"
    ]

    # Iterate over the list of Directories
    for directory in directoryList:
        if createDirectory(directory):
            print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {directory} didn't exist, but is created by ProxmoxTemplater")
        else:
            print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {directory} exists")
    
    print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] Prerequisites check completed.")


    # --- Create VM template ---
    # Store needed values in variables
    qmBin           = globalSettings.get("qm_bin")
    linuxImage      = templateSettings.get("vm_image")
    vmid            = templateSettings.get("vm_id")
    imageSize       = templateSettings.get("vm_size")
    vmName          = templateSettings.get("vm_name")
    cloudInject     = templateSettings.get("vm_inject")
    storagePool     = templateSettings.get("storage_pool")
    vmUser          = templateSettings.get("vm_user")
    sshKey          = templateSettings.get("vm_user_ssh_key")
    vmCores         = templateSettings.get("vm_cores")
    vmMem           = templateSettings.get("vm_memory")
    vmAgent         = templateSettings.get("vm_agent")
    vmNetTag        = templateSettings.get("vm_tag")
    vmNetBridge     = templateSettings.get("vm_bridge")
    debug           = templateSettings.get("debug")

    # SHOW SETTINGS USING:
    print(f"""
[{Fore.BLUE}INFO{Style.RESET_ALL}] Using settings:
       {Style.BRIGHT}Template ID:{Style.RESET_ALL} {vmid}
       {Style.BRIGHT}Template Name:{Style.RESET_ALL} {vmName}
       {Style.BRIGHT}Template Storage:{Style.RESET_ALL} {storagePool}
       {Style.BRIGHT}Cloud-Init Settings:{Style.RESET_ALL} {cloudInject}
       {Style.BRIGHT}Default user:{Style.RESET_ALL} {vmUser}
       {Style.BRIGHT}SSH Key File:{Style.RESET_ALL} {sshKey}

       {Style.BRIGHT}Base image:{Style.RESET_ALL} {linuxImage}
       {Style.BRIGHT}Image Size:{Style.RESET_ALL} {imageSize}

       {Style.BRIGHT}Using debug:{Style.RESET_ALL} {debug}"""
    )

    # Create the VM and template :-D
    newImage = imageBuilder(qmBin, linuxImage, vmid, imageSize, vmName, cloudInject, storagePool, vmUser, sshKey, vmCores, vmMem, vmAgent, vmNetTag, vmNetBridge, debug)
    newImage.createVM()
   
if __name__ == "__main__":
    main()