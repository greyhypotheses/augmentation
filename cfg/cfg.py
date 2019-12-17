import os

import dotmap
import yaml


class Cfg:

    def __init__(self):
        self.path = os.path.split(os.path.abspath(__file__))[0]

    def variables(self):
        """
        Parses the generic variables file of this project

        :return:
        """

        with open(os.path.join(self.path, 'variables.yml'), 'r') as file:
            variables = yaml.safe_load(file)

        baseline = dotmap.DotMap(variables)
        baseline.augmentation.images.strip = int(baseline.augmentation.images.remnant / 2)

        # The required image dimensions.
        dimensions = (baseline.augmentation.images.rows, baseline.augmentation.images.columns)

        # The temporary image size.  In order to avoid edge artefacts the image is resized to a
        # size slightly greater than required, then clipped after all other
        # transformation steps.
        temporary_size = (dimensions[0] + baseline.augmentation.images.remnant,
                          dimensions[1] + baseline.augmentation.images.remnant)
        baseline.augmentation.images.temporary_size = temporary_size

        # The centre point about which a rotation should occur
        rows, columns = temporary_size[0], temporary_size[1]
        baseline.augmentation.images.centre = (columns / 2, rows / 2)

        # Save
        baseline.target.images.path = os.path.join(os.path.split(os.getcwd())[0],
                                                   baseline.target.images.directory)

        return baseline

    def logs(self):
        """
        Parses the logs settings file of this project

        :return:
        """

        with open(os.path.join(self.path, 'logs.yml'), 'r') as file:
            logs = yaml.safe_load(file)

        return dotmap.DotMap(logs)
