import os

import dotmap
import yaml


class Cfg:

    def __init__(self):
        self.path = os.path.split(os.path.abspath(__file__))[0]

    def variables(self):
        """
        Parses the generic variables YAML of this project
        :return:
        """

        with open(os.path.join(self.path, 'variables.yml'), 'r') as file:
            variables = yaml.safe_load(file)

        return dotmap.DotMap(variables)

    def logs(self):
        """
        Will parse the logs YAML of this project
        :return:
        """

        return self.path
