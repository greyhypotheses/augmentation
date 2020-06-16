"""Module prepare"""
import typing

import pandas as pd


class Prepare:
    """
    Class prepare
    """

    def __init__(self, var):
        """
        Common Variables
        """

        # The images, and the rotation angles to apply per image
        self.rotations = var.augmentation.images.rotations
        self.url = var.source.images.url
        self.ext = var.source.images.ext

        # The metadata file fields that have been read-in, and the missing value replacements per field
        self.use = var.source.metadata.use
        self.if_missing = var.source.metadata.if_missing

    def image_url(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        :type data: pandas.DataFrame

        :param data: A data frame that includes an image column via which each image source URL is created
        :return:
            data: Enhanced data frame
        """

        data['image_url'] = data['image'].apply(lambda x: self.url + x + self.ext)

        return data

    def missing(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Addressing missing values.

        :type data: pandas.DataFrame

        :param data: A data frame whose missing values will be addressed
        :return:
            data: Enhanced data frame
        """

        for field in range(len(self.use)):
            data[self.use[field]] = data[self.use[field]].fillna(value=self.if_missing[field])

        for field in range(len(self.use)):
            data[self.use[field]] = data[self.use[field]].apply(lambda x: self.if_missing[field] if x == '' else x)

        return data

    def angles(self, data: pd.DataFrame, fields: typing.List, labels: typing.List) -> pd.DataFrame:
        """
        Expands the data frame such that each original image now has a row per rotation required.

        :type data: pandas.DataFrame
        :type fields: list
        :type labels: list

        :param data: A data frame
        :param fields: The columns of data that are not label/class columns
        :param labels: The label/class columns of data
        :return:
        """
        angle_fields = {'A' + str(i).zfill(3): i for i in self.rotations}

        data = data.assign(**angle_fields)
        data = data.melt(id_vars=fields + labels,
                         value_vars=list(angle_fields.keys()),
                         var_name=['angle_fields_names'],
                         value_name='angle').drop(columns=['angle_fields_names'])

        return data

    def exc(self, data: pd.DataFrame, fields: typing.List, labels: typing.List) -> pd.DataFrame:
        """
        Addresses missing data, assigns angles of rotation via angles(),
        and adds an image location/url field via image_url()

        :param data: The data frame summarising the images to be augmented and their metadata thus far
        :param fields: The non-label columns of data
        :param labels: The label columns of data
        :return:
        """

        # Missing Data
        inventory = self.missing(data)

        # Add the rotation angles field; each original image will be rotated by a set of angles
        inventory = self.angles(inventory, fields=fields, labels=labels)

        # Add image_url field
        inventory = self.image_url(inventory)

        return inventory
