import pytest

import src.data.usable as usable
import src.data.prepare as prepare

import src.federal.federal as federal


class TestPrepare:

    @pytest.fixture
    def variables(self):
        variables = federal.Federal().variables()
        rotations = variables['augmentation']['images']['rotations']
        return rotations

    @pytest.fixture
    def dataset(self):
        data, fields, labels = usable.Usable().summary()
        return data, fields, labels


    def test_summary(self, dataset):
        data, fields, labels = dataset
        data = prepare.Prepare().summary(data=data, fields=fields, labels=labels)

        counts = data[fields].count(axis=0).apply(lambda x: x == data.shape[0])
        assert all(counts), "None of the features fields should have a missing value, and hence the length " \
                            "of each must be the same as length of the data frame within which they are hosted"

        assert any(data.columns == 'angle'), "An angle of rotation field, named angle, is required"

        assert any(data.columns == 'image_url'), "An image_url field, which has the URL link to each image, " \
                                                 "is required"


    def test_angles(self, dataset, variables):
        data, fields, labels = dataset
        data = prepare.Prepare().missing(data=data)

        inventory = prepare.Prepare().angles(data=data, fields=fields, labels=labels)
        rotations = variables

        assert any(inventory.columns == 'angle')
        assert inventory.shape[0] == data.shape[0] * len(rotations)

