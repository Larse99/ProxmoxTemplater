# Proxmox and Cloud-Init template builder
# Version: V2.0.0
# Author: Lars Eissink

from classes.configReader import readYaml
from classes.argumentParser import argumentParser
from classes.imageBuilder import imageBuilder

def main():

    # Initiate argumentParser
    getArguments = argumentParser()
    cliArguments = getArguments.parse()

    # Get Settings from YAML
    getSettings = readYaml(cliArguments['config'])

    # Print configfile
    # print(cliArguments['config'])

    # Print settings
    globalSettings = getSettings.getGlobalSettings()
    templateSettings = getSettings.getTemplateSettings()

    print(globalSettings.get("qm_bin"))
    print(templateSettings.get("vmid"))





















    


if __name__ == "__main__":
    main()