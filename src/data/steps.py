import src.geometry.transform as transform
import src.io.file as file

import os

import cfg.cfg as cfg


class Steps:

    def __init__(self):
        """
        Herein, the common variables of this projects are imported for the defined steps.

        """

        # An instance of variables
        variables = cfg.Cfg().variables()

        # Remnant: Temporary extra length added to the required/target image size
        remnant = variables.image.remnant

        # Strip: The length that would subsequently be stripped off each edge of an image
        self.strip = int(remnant/2)

        # The required/target image size
        image_size = (variables.image.rows, variables.image.columns)

        # The temporary image size.  In order to avoid edge artefacts the image is resized to a size
        # slightly greater than required, then clipped after all other transformation steps.
        self.temporary_size = (image_size[0] + remnant, image_size[1] + remnant)

        # The centre point about which a rotation should occur
        rows, columns = self.temporary_size[0], self.temporary_size[1]
        self.centre = (columns/2, rows/2)

        # Save path
        self.save_path = os.path.join(os.getcwd(), variables.directories.augmented.images)

    def augment(self, filename, angle):
        """
        The image augmentation steps, which are executed via Dask

        :type filename: str
        :type angle: int [degrees]

        :param filename: The image URL String, or a string accepted by skimage.io.imread()
        :param angle: The angle of rotation, in degrees.
        :return:
        """

        # Import the image
        image = file.read(filename)

        # Transform: BGR -> RGB
        coloured = transform.colour(image)

        # Resize the image
        resized = transform.resize(tensor=coloured, dimensions=self.temporary_size)

        # Rotate the image by an angle about a centre.  Retain the image size.
        rotated = transform.rotate(tensor=resized, dimensions=self.temporary_size, centre=self.centre, angle=angle)

        # Clip the image to the required size.  In order to avoid edge artefacts the image is resized to a size
        # slightly greater than required, then clipped after all other transformation steps.
        clipped = transform.clip(tensor=rotated, strip=self.strip)

        # Create a name for the image
        image_name = file.alias(filename, angle)

        # Save
        file.save(clipped, os.path.join(self.save_path, image_name)).compute()
