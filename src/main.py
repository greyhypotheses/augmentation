"""Module main"""

import os
import sys
import argparse

import dask.array as da
import pandas as pd


def main():
    """
    main

    :return:
    """

    # Parse the expected input argument
    parser = argparse.ArgumentParser()
    parser.add_argument("image_length", type=arguments.Arguments().image_length,
                        help="The number of rows or columns of the prospective square images; "
                             "all pre-trained convolution neural network bases require square image inputs.")
    parser.add_argument("-p", "--preview", type=arguments.Arguments().preview,
                        help="Augment a specified, small, number of images")
    args = parser.parse_args()

    # Clear the current set of images
    directories.Directories().clear()

    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    inventory, fields, labels = usable.Usable().summary()

    # Prepare
    inventory = prepare.Prepare().summary(data=inventory, fields=fields, labels=labels)

    # If preview has a value
    if args.preview is not None:
        limit = args.preview
    else:
        limit = inventory.shape[0]

    # Directory for augmentations
    directories.Directories().create()

    # Augmentation
    outcomes = [generator.Generator(image_length=args.image_length).images(
        filename=image_url.compute(), angle=angle.compute()
    ) for image_url, angle in da.from_array(inventory[['image_url', 'angle']].to_numpy()[:limit], chunks=(64, 2))]
    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])

    # Save inventory, split the directory of image files into smaller directories, zip
    preserve.Preserve().steps(inventory, augmentations)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))
    import src.data.generator as generator
    import src.data.prepare as prepare
    import src.data.usable as usable
    import src.data.preserve as preserve
    import src.io.directories as directories
    import src.io.arguments as arguments
    main()
