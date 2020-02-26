import argparse
import config


class Arguments:

    def __init__(self):

        # The global variables
        variables = config.Config().variables()
        self.minimum_length = variables['augmentation']['images']['minimum_length']

        # The minimum number of images that can be requested for augmentations previewing purposes.
        # Pending: Add to global variables.
        self.number_of_images = 32

    def image_length(self, value):
        if int(value) < self.minimum_length:
            raise argparse.ArgumentTypeError("The length of each prospective square image "
                                             "must be at least {}".format(self.minimum_length))
        return int(value)

    def preview(self, value):
        if int(value) < self.number_of_images:
            raise argparse.ArgumentTypeError("The argument '--small' must be a positive integer "
                                             "greater than or equal to {}".format(self.number_of_images))
        return int(value)
