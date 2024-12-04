# Processes YAML to something Python can work with.
import yaml

class readYaml:
    """
        This class reads a .yaml file.
        This is necessary so Python can save the values in variables
        So the programm can use it.

        - getGlobalSettings:
          This method will get all the global settings. These include general specific settings.

        - getTemplateSettings:
          This will get all the Template specific settings. Stuff like vmid, image_size, name etc.
    """    

    def __init__(self, file_path):
        self.file_path = file_path

    def getGlobalSettings(self):
        # Open the configuration
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                return data.get('global_settings', {})

        except Exception as e:
            # print(f"Error while reading the Global Settings: {e}")
            return False

    def getTemplateSettings(self):
        # Open the configuration
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                return data.get('template_settings', {})
        except Exception as e:
            # print(f"Error while reading the Template Settings: {e}")
            return False