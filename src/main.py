"""Module main"""

import os
import sys
import argparse

import dask.array as da
import pandas as pd

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    import config
    import src.data.generator as generator
    import src.data.prepare as prepare
    import src.data.usable as usable
    import src.data.preserve as preserve
    import src.io.directories as directories


def main():
    """
    main

    :return:
    """

    # Parse the expected input argument
    parser = argparse.ArgumentParser()
    parser.add_argument("image_length", help="The number of rows or columns of the prospective square images; "
                                             "all pre-trained convolution neural network bases require square "
                                             "image inputs.")
    args = parser.parse_args()

    # Validate the argument's type
    try:
        isinstance(int(args.image_length), int)
        image_length = int(args.image_length)
    except TypeError as exception:
        print(exception)
        sys.exit(1)

    # Ensure that the 'image_length' argument is greater than the general minimum expected.
    variables = config.Config().variables()
    minimum_length = variables['augmentation']['images']['minimum_length']
    if image_length < minimum_length:
        raise Exception("The length of each prospective square image must be at least {}".format(minimum_length))

    # Clear the current set of images
    directories.Directories().clear()

    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    inventory, fields, labels = usable.Usable().summary()

    # Prepare
    inventory = prepare.Prepare().summary(data=inventory, fields=fields, labels=labels)

    # Directory for augmentations
    directories.Directories().create()

    # Augmentation
    outcomes = [generator.Generator(image_length=image_length).images(
        filename=image_url.compute(), angle=angle.compute()
    ) for image_url, angle in da.from_array(inventory[['image_url', 'angle']].to_numpy()[:12800], chunks=(64, 2))]
    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])

    # Save inventory, split the directory of image files into smaller directories, zip
    preserve.Preserve().steps(inventory, augmentations)


if __name__ == '__main__':
    main()
