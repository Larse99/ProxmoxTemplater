# Processes arguments and translates it to something Python can interact with.
import argparse

class argumentParser:
    """
        This class parses arguments given from the CLI.
        This is necessary so Python can save the values to variables.
        E.g. this will be used to read a configfile or override certain settings later on

        - addArguments
          This method is used to get the arguments. Here you can add/set the needed or wanted arguments
          accordingly.
        
        - parse
          This just parses the arguments.
          Or well, it also returns them as a dictionary, so we can read and use them when needed!


    """    

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Parses CLI commands to interact with Image Builder."
        )
        self.addArguments()

    def addArguments(self):
        """ The arguments that will be accepted from the CLI """
        self.parser.add_argument(
            "-c", "--config",
            type=str,
            help="Path to configuration file",
            required=True
        )

        self.parser.add_argument(
            "-o", "--override",
            type=str,
            nargs="+",
            help="Override a value. Format: key=value"
        )

        # Parse ideas:
        # - Debug
        # - CI Injection File
        # - ...

    def parse(self):
        """ Parse the arguments and return them as a dictionary. """
        args = self.parser.parse_args()

        # Process overrides, if there are any
        overrides = {}
        if args.override:
            for override in args.override:
                key, value = override.split("=", 1)
                overrides[key] = value
        
        # Return the dictionary
        return {
            "config": args.config,
            "overrides": overrides
        }