"""Module images"""
import logging
import multiprocessing as mp

import pandas as pd
import requests

import src.federal.federal as federal


class Images:
    """
    Class Images
    Tests the existence of a random set of images
    """

    def __init__(self):
        """
        The constructor
        """

        # Logging
        federal.Federal().logs()
        self.logger = logging.getLogger('debug')
        self.logger.name = __name__

        # Variables
        variables = federal.Federal().variables()
        self.url = variables['source']['images']['url']
        self.ext = variables['source']['images']['ext']
        self.tests_random_sample_size = variables['tests']['random_sample_size']


    def state(self, image):
        """

        :param image:
        :return:
        """

        # Image
        req = requests.get(self.url + image + self.ext)

        # Return image & access status code
        return {'image': image, 'status': 1 if req.status_code == 200 else 0}

    def states(self, images):
        """
        :type images: pandas.Series

        :param images:
        :return:
        """

        # Parallel Processing via CPU
        pool = mp.Pool(mp.cpu_count())

        # For a small data frame of image names
        # images.sample(n=config.variables['tests']['random_sample_size']['images'])
        excerpt: pd.Series = images.sample(n=self.tests_random_sample_size)

        # An iterable form of excerpt
        # [{excerpt[i]} for i in excerpt.index]
        excerpt_iterable = excerpt.tolist()

        # Determine whether each of the randomly selected images exists in the repository
        # image, status
        sample_dict = pool.starmap_async(Images.state, [i for i in excerpt_iterable]).get()
        sample_frame = pd.DataFrame(sample_dict)

        # Are there any missing images?
        missing_images = sample_frame[sample_frame.status == 0]
        self.logger.info(missing_images)

        # The status codes of the images
        return sample_frame
