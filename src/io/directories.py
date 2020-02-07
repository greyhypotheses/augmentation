import os

import config as config


class Directories:

    def __init__(self):

        self.name = 'Directories'

        # Variables
        variables = config.Config().variables()
        self.path = variables['target']['path']
        self.images_path = variables['target']['images']['path']
        self.splits_path = variables['target']['splits']['path']
        self.zips_path = variables['target']['zips']['path']

    def clear(self):
        """
        Deleting all images & directories within the images directory
        :return:
        """

        images_ = [os.remove(os.path.join(base, file))
                   for base, directories, files in os.walk(self.path)
                   for file in files]

        if any(images_):
            raise Exception(
                "Unable to delete all the files within the directories/sub-directories of {}".format(self.path))

        directories_ = [os.removedirs(os.path.join(base, directory))
                        for base, directories, files in os.walk(self.path, topdown=False)
                        for directory in directories
                        if os.path.exists(os.path.join(base, directory))]

        if any(directories_):
            raise Exception("Unable to delete all the directories/sub-directories within {}".format(self.path))

    def create(self):

        # Directories for augmentations
        for i in [self.path, self.images_path, self.splits_path, self.zips_path]:
            if not os.path.exists(i):
                os.makedirs(i)
