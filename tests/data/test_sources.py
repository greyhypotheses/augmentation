import pytest

import src.data.sources
import src.data.sources
import src.io.arguments
import src.io.arguments


class TestSources:

    @pytest.fixture()
    def var(self):
        arguments = src.io.arguments.Arguments()
        urlstring = 'https://raw.githubusercontent.com/greyhypotheses/dictionaries/develop/augmentation/variables.yml'

        req = arguments.url(urlstring)
        return arguments.parameters(req)

    @pytest.fixture()
    def sources(self, var):
        return src.data.sources.Sources(var=var)

    def test_truth(self, sources, var):
        truth_use = var.source.truth.use

        truth = sources.truth()
        assert truth.shape[0] != 0, "The ground truth labels file should not be empty"
        assert set(truth.columns) == set(truth_use), "The columns of truth must be those " \
                                                     "specified in variables.yml"

    def test_metadata(self, sources, var):
        metadata_use = var.source.metadata.use

        metadata = sources.metadata()
        assert metadata.shape[0] != 0, "The metadata file should not be empty"
        assert set(metadata.columns) == set(metadata_use), "The columns of metadata must be those " \
                                                           "specified in variables.yml"

    def test_exc(self, sources, var):
        truth_use = var.source.truth.use
        truth_key = var.source.truth.key
        metadata_use = var.source.metadata.use

        truth = sources.truth()
        metadata = sources.metadata()
        inventory, fields, labels = sources.exc()

        assert truth.shape[0] == inventory.shape[0], "The number of ground truth & inventory data points must be equal"
        assert metadata.shape[0] == inventory.shape[0], "The number of medata & inventory data points must be equal"

        assert set([truth_key] + labels) == set(truth_use), "The values of labels do not match the labels of truth"
        assert set(fields) == set(metadata_use), "A values of fields don't match the uploaded columns of metadata"

        assert inventory.image.unique().shape[0] == inventory.shape[0], "Each image name can occur once only"
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"
