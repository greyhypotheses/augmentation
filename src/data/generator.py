"""Module generator"""
import os

import dask

import config
import src.geometry.transform as transform
import src.io.images as images


class Generator:
    """
    Class Generator
    """

    def __init__(self, image_length: int):
        """
        Common variables
        """

        # An instance of variables
        variables = config.Config().variables()

        # Strip: The length that would subsequently be stripped off each edge of an image
        self.strip = variables['augmentation']['images']['strip']

        # The temporary image size.  In order to avoid edge artefacts the image is resized to a
        # size slightly greater than required, then clipped after all other
        # transformation steps.
        dimensions = (image_length, image_length)
        self.temporary_size = (dimensions[0] + variables['augmentation']['images']['remnant'],
                               dimensions[1] + variables['augmentation']['images']['remnant'])

        # The centre point about which a rotation should occur
        rows, columns = self.temporary_size[0], self.temporary_size[1]
        self.centre = (columns / 2, rows / 2)

        # Save path
        self.path = variables['target']['images']['path']

    def augment(self, image, angle):
        """
        :type image: numpy.ndarray
        :type angle: int

        :param image:
        :param angle:
        :return:
        """

        # Transform: BGR -> RGB
        coloured = transform.colour(image)

        # Resize the image
        resized = transform.resize(tensor=coloured, dimensions=self.temporary_size)

        # Rotate the image by an angle about a centre.  Retain the image size.
        rotated = transform.rotate(tensor=resized, dimensions=self.temporary_size, centre=self.centre, angle=angle)

        # Clip the image to the required size.  In order to avoid edge artefacts the image is resized to a size
        # slightly greater than required, then clipped after all other transformation steps.
        clipped = transform.clip(tensor=rotated, strip=self.strip)

        # Return
        return clipped

    def images(self, filename, angle):
        """
        The image augmentation steps, which are executed via Dask

        :type filename: str
        :type angle: int [degrees]

        :param filename: The image URL String, or a string accepted by skimage.io.imread()
        :param angle: The angle of rotation, in degrees.
        :return:
        """

        # Import the image
        image = images.read(filename)

        # Augment the image
        augmented = self.augment(image, angle)

        # Create a name for the image
        image_name = images.alias(filename, angle)

        # Save
        state = dask.compute(images.save(augmented, os.path.join(self.path, image_name)))

        # Return
        return image_name, image_name.split('-', 1)[0], angle, state.__getitem__(0)
