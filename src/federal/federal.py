import os

import yaml


class Federal:

    def __init__(self):
        self.path = os.path.split(os.path.abspath(__file__))[0]

    def variables(self):
        """
        Parses the generic variables file of this project

        :return:
        """

        with open(os.path.join(self.path, 'variables.yml'), 'r') as file:
            variables = yaml.safe_load(file)

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

        # Save
        variables['target']['images']['path'] = os.path.join(os.getcwd(),
                                                             variables['target']['images']['directory'])

        return variables

    def logs(self):
        """
        Parses the logs settings file of this project

        :return:
        """

        with open(os.path.join(self.path, 'logs.yml'), 'r') as file:
            logs = yaml.safe_load(file)

        return logs
