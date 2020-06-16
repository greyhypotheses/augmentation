import pytest

import src.data.preliminaries
import src.data.prepare
import src.io.arguments


class TestPrepare:

    @pytest.fixture()
    def var(self):
        arguments = src.io.arguments.Arguments()
        urlstring = 'https://raw.githubusercontent.com/greyhypotheses/dictionaries/develop/augmentation/variables.yml'

        req = arguments.url(urlstring)
        return arguments.parameters(req)

    @pytest.fixture()
    def prepare(self, var):
        return src.data.prepare.Prepare(var=var)

    @pytest.fixture
    def dataset(self, var):
        data, fields, labels = src.data.preliminaries.Preliminaries(var=var).exc()
        return data, fields, labels

    def test_angles(self, dataset, prepare, var):
        data, fields, labels = dataset
        data = prepare.missing(data=data)

        inventory = prepare.angles(data=data, fields=fields, labels=labels)
        rotations = var.augmentation.images.rotations

        assert any(inventory.columns == 'angle')
        assert inventory.shape[0] == data.shape[0] * len(rotations)

    def test_exc(self, dataset, prepare):
        data, fields, labels = dataset
        data = prepare.exc(data=data, fields=fields, labels=labels)

        counts = data[fields].count(axis=0).apply(lambda x: x == data.shape[0])
        assert all(counts), "None of the features fields should have a missing value, and hence the length " \
                            "of each must be the same as length of the data frame within which they are hosted"

        assert any(data.columns == 'angle'), "An angle of rotation field, named angle, is required"

        assert any(data.columns == 'image_url'), "An image_url field, which has the URL link to each image, " \
                                                 "is required"
