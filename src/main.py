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

    # Clear the current set of images
    directories.clear()

    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    inventory, fields, labels = preliminaries.exc()

    # Prepare
    inventory = prepare.exc(data=inventory, fields=fields, labels=labels)

    # If preview has a value
    if args.sample is not None:
        limit = args.sample
    else:
        limit = inventory.shape[0]

    # Directory for augmentations
    directories.create()

    # Augmentation
    outcomes = [generator.exc(filename=image_url.compute(), angle=angle.compute())
                for image_url, angle
                in da.from_array(inventory[['image_url', 'angle']].to_numpy()[:limit], chunks=(64, 2))]
    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])

    # Save inventory, split the directory of image files into smaller directories, zip
    write.exc(inventory, augmentations)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))
    import src.data.generator
    import src.data.prepare
    import src.data.preliminaries
    import src.data.write
    import src.io.directories
    import src.io.arguments

    # Parse the expected input argument
    arguments = src.io.arguments.Arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument('elements',
                        type=arguments.url,
                        help='The URL of a YAML of parameters; refer to the README notes.  The argument '
                             'parser returns a blob of elements')
    parser.add_argument("--sample", type=arguments.sample,
                        help="Augment a specified, small, number of images")
    args = parser.parse_args()

    # Get the data parameters encoded by the input
    var = arguments.parameters(elements=args.elements)

    # Instances
    directories = src.io.directories.Directories(var=var)
    preliminaries = src.data.preliminaries.Preliminaries(var=var)
    prepare = src.data.prepare.Prepare(var=var)
    generator = src.data.generator.Generator(var=var)
    write = src.data.write.Write(var=var)

    main()
