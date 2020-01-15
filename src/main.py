"""Module main"""

import os
import sys

import dask.array as da
import pandas as pd

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(), 'src'))
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

    # Clear the current set of images
    directories.Directories().clear()

    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    inventory, fields, labels = usable.Usable().summary()

    # Prepare
    inventory = prepare.Prepare().summary(data=inventory, fields=fields, labels=labels)

    # Unnecessary augmentations
    inventory = inventory.loc[~((inventory.NV == 1) & (inventory.angle > 0))]
    inventory.reset_index(inplace=True, drop=True)

    # Directory for augmentations
    directories.Directories().create()

    # Augmentation
    outcomes = [generator.Generator().images(filename=image_url.compute(), angle=angle.compute())
                for image_url, angle in da.from_array(inventory[['image_url', 'angle']].to_numpy(), chunks=64)]

    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])

    # Save inventory, split the directory of image files into smaller directories, zip
    preserve.Preserve().steps(inventory, augmentations)


if __name__ == '__main__':
    main()
