"""Module sources"""
import sys

import pandas as pd

import src.federal.federal as federal


class Sources:
    """
    Class Source
    """

    def __init__(self):
        """

        """
        variables = federal.Federal().variables()
        self.truth_url = variables['source']['truth']['url']
        self.truth_use = variables['source']['truth']['use']
        self.truth_key = variables['source']['truth']['key']
        self.metadata_url = variables['source']['metadata']['url']
        self.metadata_use = variables['source']['metadata']['use']
        self.metadata_key = variables['source']['metadata']['key']

    def truth(self):
        """
        Reads the ground truth data file.  The location of the file is recorded
        in the 'configurations/variables.json' file
        :return:
            truth: A data frame of the data in the file
        """
        try:
            truth = pd.read_csv(self.truth_url, usecols=self.truth_use)
        except OSError as error:
            print(error)
            sys.exit(1)

        return truth

    def metadata(self):
        """
        Reads the metadata data file.  The location of the file is recorded
        in the 'configurations/variables.json' file
        :return:
            metadata: A data frame of the data in the file
        """
        try:
            metadata = pd.read_csv(self.metadata_url, usecols=self.metadata_use)
        except OSError as error:
            print(error)
            sys.exit(1)

        return metadata

    def summary(self):
        """
        Reads the 'truth' & 'metadata' files and joins their data via the image name field 'image'
        :return:
            inventory: The joined 'truth' & 'metadata' data
            labels: The list of the data's classes; the classes are one-hot-coded.
            fields: The list of metadata fields, excluding labels.
        """
        truth = Sources().truth()
        metadata = Sources().metadata()

        # Join the metadata & truth data frames via common field 'image'
        inventory = metadata.merge(truth, left_on=self.metadata_key, right_on=self.truth_key, how='inner')
        inventory.drop_duplicates(keep='first', inplace=True)

        # The truth labels are one-hot-coded.  The labels are
        labels = truth.columns.drop(self.truth_key).values.tolist()
        inventory[labels] = inventory[labels].astype('int')

        # The metadata fields, including the key
        fields = inventory.columns.drop(labels).values.tolist()

        # Herein,
        #   the class/label fields are selected: inventory[labels]
        #   then the sum-per-row is calculated: inventory[labels].sum(axis=1)
        # If each image is associated with a single class then the sum of each row will be 1, i.e.,
        #   inventory[labels].sum(axis=1).all() will be True
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"

        # Hence
        return inventory, labels, fields
