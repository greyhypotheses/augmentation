"""Module image"""
import io

import matplotlib.image as image
import numpy as np
import requests

import src.cfg.cfg as cfg


class Image:
    """
    Class Image
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self.name = 'Images'

    @staticmethod
    def name(images, datawidth, index):
        """
        Extract image name
        :param images: A data frame of image names.  Each column name is an image class name, and each column records
                       a series of image names.
        :param datawidth: The number of columns of images [In progress, remove]
        :param index: The index of a series of images
        :return:
                image name
        """
        # Extracting image names via table grid
        return images.loc[np.floor(index / datawidth).astype(int), images.columns[np.mod(index, datawidth)]]

    @staticmethod
    def data(images, datawidth, index):
        """

        :param images: A data frame of image names wherein the column names are the lesion types.
        :param datawidth: The width of images, i.e., the number of columns
        :param index: The ith image in focus
        :return:
            image data for drawing
            image name
        """

        # Extracting an image name
        name = Image.name(images, datawidth, index)

        # Image URL
        url = cfg.Cfg().variables()['source']['images']['url'] + name + cfg.Cfg().variables()['source']['images']['ext']

        # Get Image
        r = requests.get(url)
        return image.imread(io.BytesIO(r.content), format='jpeg')

    @staticmethod
    def draw(handle, images, datawidth, index, figrows, figcolumns):
        """
        Draw the image using ...
        :param handle: The graph handle w.r.t. fig, handle = matplotlib.plotly.subplots()
        :param images: A data frame of image names wherein the column names are the lesion types.
        :param datawidth: The width of images, i.e., the number of columns
        :param index: The ith image in focus
        :param figrows: The number of rows in the fig grid
        :param figcolumns: The number of columns in the fig grid
        :return:
        """

        # The
        name = Image.name(images, datawidth, index)

        # An image's raw data
        data = Image.data(images, datawidth, index)

        # Calculating a figure grid location
        n = np.floor_divide(index, figrows)
        m = np.mod(index, figcolumns)

        # Place Image
        handle[n, m].imshow(data)
        handle[n, m].tick_params(axis='both', labelsize='medium')
        handle[n, m].set_xlabel(name, fontsize='medium')
        handle[n, m].set_title(images.columns[np.mod(index, datawidth)], fontsize='medium')
        handle[n, m].axes.get_yaxis().set_visible(False)
        handle[n, m].axes.get_xaxis().set_ticks([])
