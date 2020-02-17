import os
import requests
import yaml
import sys


class Config:
    """
    Consists of methods that parse the global settings summarised in the online
    YAML dictionaries
    """

    def __init__(self):
        """
        The constructor
        """
        self.root = os.path.abspath(__package__)

    def paths(self, partitions):
        """
        Creates a path relative to the project's root directory
        :param partitions:
        :return:
            path: The created from a list of directories
        """

        path = self.root
        for partition in partitions:
            path = os.path.join(path, partition)

        return path

    def variables(self) -> dict:
        """
        Parses the generic variables file of this project

        :return:
        """

        url = 'https://raw.githubusercontent.com/greyhypotheses/dictionaries/develop/augmentation/variables.yml'
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        variables = yaml.safe_load(req.text)

        variables['augmentation']['images']['strip'] = int(variables['augmentation']['images']['remnant'] / 2)

        # Paths
        variables['target']['path'] = self.paths(variables['target']['directory'])
        variables['target']['images']['path'] = self.paths(variables['target']['images']['directory'])
        variables['target']['splits']['path'] = self.paths(variables['target']['splits']['directory'])
        variables['target']['zips']['path'] = self.paths(variables['target']['zips']['directory'])

        return variables

    @staticmethod
    def logs() -> dict:
        """
        Parses the logs settings file of this project

        :return:
        """

        url = 'https://raw.githubusercontent.com/greyhypotheses/dictionaries/develop/derma/logs.yml'
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        logs = yaml.safe_load(req.text)

        return logs
