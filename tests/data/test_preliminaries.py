import src.data.preliminaries
import src.io.arguments
import pytest


class TestPreliminaries:

    @pytest.fixture()
    def var(self):
        arguments = src.io.arguments.Arguments()
        urlstring = 'https://raw.githubusercontent.com/greyhypotheses/dictionaries/develop/augmentation/variables.yml'

        req = arguments.url(urlstring)
        return arguments.parameters(req)

    @pytest.fixture()
    def preliminaries(self, var):
        return src.data.preliminaries.Preliminaries(var=var)

    @pytest.fixture()
    def dataset(self, preliminaries):
        data, fields, labels = preliminaries.exc()
        return data, fields, labels

    def test_instances(self, dataset, preliminaries):
        inventory, fields, labels = dataset
        summary = preliminaries.instances(inventory, labels)
        assert summary.sum() == inventory[labels].sum(axis=0).sum()

    def test_exc(self, dataset):
        inventory, fields, labels = dataset

        assert len(labels) != 0, "At least one label column must exist"
        assert len(fields) != 0, "Missing field names"
        assert inventory.image.unique().shape[0] == inventory.shape[0], "Each image name can occur once only"
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"
