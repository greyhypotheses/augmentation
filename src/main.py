"""Module main"""

import os
import sys

import dask.array as da
import pandas as pd

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    import src.data.generator as generator
    import src.cfg.cfg as cfg
    import src.data.prepare as prepare
    import src.data.usable as usable
    import src.io.directories as dir


def main():
    """
    main

    :return:
    """

    # Clear the current set of images
    dir.Directories().clear()

    # Variables
    variables = cfg.Cfg().variables()
    path = variables['target']['images']['path']

    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    use = usable.Usable()
    inventory, labels, fields = use.summary()

    # Prepare
    prep = prepare.Prepare()
    inventory = prep.missing(inventory)
    inventory = prep.angles(inventory, labels=labels, fields=fields)

    # Unnecessary augmentations
    inventory = inventory.loc[~((inventory.NV == 1) & (inventory.angle > 0))]
    inventory.reset_index(inplace=True)

    # Image URL
    inventory = prep.filename(inventory)

    # Development: This snippet will be deleted after the development phase
    development = True
    if development:
        inventory = inventory.groupby(['AK', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'SCC', 'VASC'])[inventory.columns.tolist()] \
            .apply(lambda x: x.sample(n=160, replace=False, random_state=5))
        inventory.reset_index(drop=True, inplace=True)

    # Directory for augmentations
    dir.Directories().create()

    # Augmentation
    template = inventory[['filename', 'angle']]

    outcomes = [generator.Generator().images(filename=filename.compute(), angle=angle.compute())
                for filename, angle in da.from_array(template.to_numpy(), chunks=64)]

    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])
    focus = inventory.merge(augmentations, how='inner', on=['image', 'angle']).drop(columns=['filename', 'index'])

    # Write
    # Automate directories for zipping via https://docs.python.org/3.7/library/shutil.html
    focus.to_csv(os.path.join(path, 'inventory.csv'), index=False)


if __name__ == '__main__':
    main()
