"""Module usable"""
import logging
import typing

import pandas as pd

import config
import src.data.sources as sources


class Usable:
    """
    An extension of sources. It eliminates a class/label, and its records, if the class' sample size
    is < minimum_class_instances
    """

    def __init__(self):
        """
        Constructor
        """

        config.Config().logs()
        self.logger = logging.getLogger('debug')
        self.logger.disabled = True
        self.logger.name = __name__

        variables = config.Config().variables()
        self.minimum_class_instances = variables['modelling']['minimum_class_instances']

    def instances(self, dataset: pd.DataFrame, labels: list) -> pd.Series:
        """
        This method calculates the number of instances/records per class w.r.t. a data set
        whose labels have been one-hot-coded.

        :param dataset: A data frame of data
        :param labels: The list of one-hot-coded label columns in dataset

        :return:
            summary: A pandas series that records the number of instances per class; it has a class names index.
        """

        # Calculate the number of instances/records per class
        summary: pd.Series = dataset[labels].sum()

        # Log the details
        self.logger.info("Instances per class:\n\n %s", summary)

        # Return
        return summary

    def outliers(self, instances_per_class: pd.Series) -> pd.Series:
        """
        :param instances_per_class: A pandas series of

        :return:
            summary: outlying classes
        """

        # The minimum number of instances, i.e., data points, required
        # per class.  Presently based on the minimum number of instances per class
        # required for the stratification of imbalanced data sets w.r.t. SciKit Learn, etc.
        minimum_class_instances = self.minimum_class_instances

        # Hence, are there any outlying classes?
        summary: pd.Series = instances_per_class[instances_per_class < minimum_class_instances]

        # Log the details
        self.logger.info("Outliers:\n\n %s", summary)

        return summary

    def summary(self) -> (pd.DataFrame, typing.List, typing.List):
        """
        Reads sources.Sources().summary()
        :return:
            inventory: Excludes classes that have a sample size < minimum_class_instances; all records associated
            with the excluded classes are deleted.
            labels: The classes remaining if any had to be excluded.
            fields: The unchanged metadata fields.
        """

        # The metadata & ground truth (inventory), the names of the label columns, and
        # the names of the metadata fields
        inventory, fields, labels = sources.Sources().summary()

        # In terms of the data in question, how many instances are there per class?
        instances_per_class: pd.Series = self.instances(dataset=inventory, labels=labels)

        # Hence, outlying classes
        outlying_classes: pd.Series = self.outliers(instances_per_class)

        # The inadmissible records, i.e., rows.  Herein, we are
        # determining the rows that belong to outlying classes.
        inadmissible: pd.Int64Index = inventory[inventory[outlying_classes.index.values].any(axis=1)].index

        # Hence, admissible
        admissible: pd.DataFrame = inventory.drop(inadmissible, axis=0).drop(outlying_classes.index.values, axis=1)

        # The latest set of labels
        # [labels.remove(i) for i in outlying_classes.index.values]
        labels = sorted(list(set(labels).difference(set(outlying_classes.index.values))))

        # If yes, the associated rows & columns are dropped.
        return admissible, fields, labels
