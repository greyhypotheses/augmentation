"""Module preserve"""
import glob
import math
import os
import shutil
import zipfile
import pandas as pd

import src.federal.federal as federal


class Preserve:
    """
    Class Preserve

    This class ensures that after the image augmentations process the
        * image files are split into smaller sets, i.e., into directories, such that the zipped
          forms of these directories are appropriate for fast & parallel fetching and unzipping

        * metadata details of each image in a single csv file
    """

    def __init__(self):

        variables = federal.Federal().variables()

        # Paths
        self.path = variables['target']['path']
        self.images_path = variables['target']['images']['path']
        self.splits_path = variables['target']['splits']['path']
        self.zips_path = variables['target']['zips']['path']

        # Number of images per split; for zipping purposes
        self.images_per_split = variables['target']['splits']['images_per_split']


    def splitting(self, image_name: str, image_index: int) -> None:
        """
        Copy's an image file to its appropriate split

        :type image_name: str
        :type image_index: int

        :param image_name: The name of the image to be copied
        :param image_index: The index/identification number of the directory it will be copied to
        :return:
        """

        # Create new directory if necessary
        subdirectory = os.path.join(self.splits_path,
                                    '{0:03d}'.format(math.floor(image_index / self.images_per_split)))
        if not os.path.exists(subdirectory):
            os.mkdir(subdirectory)

        # Copy file to subdirectory
        shutil.copy(image_name, subdirectory)


    def zipping(self, directory: str) -> None:
        """
        :type directory: str

        :param directory: The name of the directory that will be zipped
        :return:
            None
        """

        # The archive name will be the raw directory name
        archive_name = os.path.basename(directory)

        # Open ...
        zip_object = zipfile.ZipFile(os.path.join(self.zips_path, archive_name + '.zip'), 'x')

        # The list of images in 'directory'
        images = glob.glob(os.path.join(directory, '*.png'))

        # Write each image in the list to a zip archive
        try:
            [zip_object.write(filename=images[i], arcname=os.path.basename(images[i]),
                              compress_type=zipfile.ZIP_DEFLATED) for i in range(len(images))]
        except OSError as err:
            print("OS Error: {0}".format(err))
            raise

        zip_object.close()


    def steps(self, inventory: pd.DataFrame, augmentations: pd.DataFrame) -> None:
        """
        :type inventory: pd.DataFrame
        :type augmentations: pd.DataFrame

        :param inventory: The inventory of the images sent-off for augmentation
        :param augmentations: The augmentation process output
        :return:
            None
        """

        # Join
        focus = inventory.merge(augmentations, how='inner', on=['image', 'angle']).drop(columns=['image_url'])
        focus.to_csv(os.path.join(self.path, 'inventory.csv'), index=False)

        # Split
        list_of_images = glob.glob(os.path.join(self.images_path, '*.png'))
        unique_id = list(range(len(list_of_images)))
        images_ = [list(x) for x in zip(list_of_images, unique_id)]
        splitting_states = [Preserve().splitting(image_name, image_index) for image_name, image_index in images_]

        # Zip
        if any(splitting_states):
            raise Exception("The splitting ...")
        else:
            directories_of_splits = glob.glob(os.path.join(self.splits_path, '*'))
            [Preserve().zipping(i) for i in directories_of_splits]
