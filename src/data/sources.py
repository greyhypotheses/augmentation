"""Module sources"""
import sys
import typing

import pandas as pd


class Sources:
    """
    Class Sources
    """

    def __init__(self, var):
        """
        Herein, the constructor initialises a set of the global/config variables.  The variables are
        defined in src/config/variables.yml
        """

        self.truth_url = var.source.truth.url
        self.truth_use = var.source.truth.use
        self.truth_key = var.source.truth.key
        self.metadata_url = var.source.metadata.url
        self.metadata_use = var.source.metadata.use
        self.metadata_key = var.source.metadata.key

    def truth(self) -> pd.DataFrame:
        """
        Reads the ground truth data file.  The location of the file is recorded
        in the 'config/variables.yml' file
        :return:
            truth: A data frame of the data in the file
        """
        try:
            truth = pd.read_csv(self.truth_url, usecols=self.truth_use)
        except OSError as error:
            print(error)
            sys.exit(1)

        return truth

    def metadata(self) -> pd.DataFrame:
        """
        Reads the metadata data file.  The location of the file is recorded
        in the 'config/variables.yml' file

        :return:
            metadata: A data frame of the data in the file
        """
        try:
            metadata = pd.read_csv(self.metadata_url, usecols=self.metadata_use)
        except OSError as error:
            print(error)
            sys.exit(1)

        return metadata

    def exc(self):
        """
        Reads the 'truth' & 'metadata' files and joins their data via the image name field 'image'
        :return:
            inventory: The joined 'truth' & 'metadata' data
            labels: The list of the data's classes; the classes are one-hot-coded.
            fields: The list of metadata fields, excluding labels.
        """
        truth: pd.DataFrame = self.truth()
        metadata: pd.DataFrame = self.metadata()

        # Join the metadata & truth data frames via common field 'image'
        inventory: pd.DataFrame = metadata.merge(truth, left_on=self.metadata_key, right_on=self.truth_key, how='inner')
        inventory.drop_duplicates(keep='first', inplace=True)

        # The truth labels are one-hot-coded.  The labels are
        labels: typing.List = truth.columns.drop(self.truth_key).values.tolist()
        inventory[labels] = inventory[labels].astype('int')

        # The metadata fields, including the key
        fields: typing.List = inventory.columns.drop(labels).values.tolist()

        # Herein,
        #   the class/label fields are selected: inventory[labels]
        #   then the sum-per-row is calculated: inventory[labels].sum(axis=1)
        # If each image is associated with a single class then the sum of each row will be 1, i.e.,
        #   inventory[labels].sum(axis=1).all() will be True
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"

        # Hence
        return inventory, fields, labels
