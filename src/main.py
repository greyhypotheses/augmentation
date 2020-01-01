"""Module main"""

import glob
import logging
import multiprocessing as mp
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


def main():
    """
    main

    :return:
    """

    # Variables
    variables = cfg.Cfg().variables()
    path = variables['target']['images']['path']

    # Logging
    # logging.basicConfig(level=logging.DEBUG)
    logging.disable(logging.DEBUG)
    logger = logging.getLogger(__name__)

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

    # Delete existing augmentations
    pool = mp.Pool(mp.cpu_count())
    images_list = glob.glob(os.path.join(path, '*.png'))
    images_iterable = [{images_list[i]} for i in range(len(images_list))]
    pool.starmap(os.remove, images_iterable)

    # Augment
    if not os.path.exists(path):
        os.makedirs(path)

    template = inventory[['filename', 'angle']]
    outcomes = [generator.Generator().images(filename=filename.compute(), angle=angle.compute())
                for filename, angle in da.from_array(template.to_numpy()[:64], chunks=32)]

    augmentations = pd.DataFrame(outcomes, columns=['name', 'image', 'angle', 'drawn'])
    focus = inventory.merge(augmentations, how='inner', on=['image', 'angle']).drop(columns=['filename', 'index'])
    logger.info(focus.head())

    # Write
    # Automate directories for zipping via https://docs.python.org/3.7/library/shutil.html
    focus.to_csv(os.path.join(path, 'inventory.csv'), index=False)


if __name__ == '__main__':
    main()
