import glob
import os

import dask.array as da

import cfg.cfg as cfg
import src.data.generator as generator
import src.data.prepare as prepare
import src.data.usable as usable


def main():
    # A summary of images metadata & labels, a list of the label fields, and a list of the metadata fields
    u = usable.Usable()
    inventory, labels, fields = u.summary()

    # Prepare
    p = prepare.Prepare()
    inventory = p.missing(inventory)
    inventory = p.angles(inventory, labels=labels, fields=fields)

    # Names
    variables = cfg.Cfg().variables()
    template = inventory[['image', 'angle']].sample(n=64, random_state=5)
    template['filename'] = template.image. \
        apply(lambda x: variables.source.images.url + x + variables.source.images.ext)

    # Existing augmentations
    states = [os.remove(f) for f in glob.glob(os.path.join(variables.target.images.path, '*.png'))]
    print(states)

    # Augment
    for image, angle, filename in da.from_array(template.to_numpy(), chunks=16):
        generator.Generator().images(filename=filename.compute(), angle=angle.compute())


if __name__ == '__main__':
    main()
