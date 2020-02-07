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

        # The required image dimensions.
        dimensions = (variables['augmentation']['images']['rows'], variables['augmentation']['images']['columns'])

        # The temporary image size.  In order to avoid edge artefacts the image is resized to a
        # size slightly greater than required, then clipped after all other
        # transformation steps.
        temporary_size = (dimensions[0] + variables['augmentation']['images']['remnant'],
                          dimensions[1] + variables['augmentation']['images']['remnant'])
        variables['augmentation']['images']['temporary_size'] = temporary_size

        # The centre point about which a rotation should occur
        rows, columns = temporary_size[0], temporary_size[1]
        variables['augmentation']['images']['centre'] = (columns / 2, rows / 2)

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
