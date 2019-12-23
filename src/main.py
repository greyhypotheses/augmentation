"""Module main"""

import glob
import logging
import os
import sys
import subprocess
import platform

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
    # del *.png, sudo rm *.png
    # del *.zip, sudo rm *.png
    n_images = glob.glob(os.path.join(path, '*.png'))

    if len(n_images) > 0:
        if platform.system() == 'Windows':
            subprocess.Popen('del ' + os.path.join(path, '*.png'), shell=True, stdout=subprocess.PIPE)
        else:
            subprocess.Popen('sudo rm ' + os.path.join(path, '*.png'), shell=True, stdout=subprocess.PIPE)

    # for file in glob.glob(os.path.join(path, '*.png')):
    #     os.remove(file)

    # Augment
    template = inventory[['filename', 'angle']]
    outcomes = [generator.Generator().images(filename=filename.compute(), angle=angle.compute())
                for filename, angle in da.from_array(template.to_numpy()[:64], chunks=16)]

    augmentations = pd.DataFrame(outcomes, columns=['image', 'angle', 'drawn'])
    focus = inventory.merge(augmentations, how='inner', on=['image', 'angle']).drop(columns=['filename'])
    logger.info(focus.head())

    # Write
    focus.to_csv(os.path.join(path, 'inventory.csv'))


if __name__ == '__main__':
    main()
