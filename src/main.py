import glob
import logging
import os

import dask.array as da
import pandas as pd

import cfg.cfg as cfg
import src.data.generator as generator
import src.data.prepare as prepare
import src.data.usable as usable


class Main:

    def __init__(self):
        self.name = 'Main'

        variables = cfg.Cfg().variables()
        self.path = variables['target']['images']['path']

    def main(self):

        # Logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
        use = usable.Usable()
        inventory, labels, fields = use.summary()

        # Prepare
        prep = prepare.Prepare()
        inventory = prep.missing(inventory)
        inventory = prep.angles(inventory, labels=labels, fields=fields)
        inventory = prep.outliers(inventory)
        inventory = prep.filename(inventory)
        logger.info(inventory.shape)
        logger.info(inventory.info())

        # Delete existing augmentations
        for f in glob.glob(os.path.join(self.path, '*.png')):
            os.remove(f)

        # Augment
        template = inventory[['filename', 'angle']]
        outcomes = [generator.Generator().images(filename=filename.compute(), angle=angle.compute())
                    for filename, angle in da.from_array(template.to_numpy()[:128], chunks=16)]

        augmentations = pd.DataFrame(outcomes, columns=['image', 'angle', 'drawn'])
        focus = inventory.merge(augmentations, how='inner', on=['image', 'angle']).drop(columns=['filename'])
        logger.info(focus.head())

        # Write
        focus.to_csv('inventory.csv')


if __name__ == '__main__':
    Main().main()
