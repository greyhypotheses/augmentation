import src.geometry.transform as transform
import src.io.file as file

import os

import configurations.configurations as cfg


class Steps:

    def __init__(self):
        self.remnant = cfg.variables['image']['remnant']
        self.strip = int(self.remnant/2)

        image_size = (cfg.variables['image']['rows'], cfg.variables['image']['columns'])
        self.temporary_size = (image_size[0] + self.remnant, image_size[1] + self.remnant)

        rows, columns = self.temporary_size[0], self.temporary_size[1]
        self.centre = (columns/2, rows/2)
        self.rotations = cfg.variables['image']['rotations']

    def augment(self, filename):

        image = file.read(filename=filename)
        resized = transform.resize(tensor=image, dimensions=self.temporary_size).compute()

        for angle in self.rotations:
            rotated = transform.rotate(tensor=resized, dimensions=self.temporary_size,
                                       centre=self.centre, angle=angle).compute()
            clipped = transform.clip(tensor=rotated, strip=self.strip).compute()
            image_name = file.alias(filename, angle).compute()
            file.save(clipped, os.path.join('augmentations', image_name)).compute()

