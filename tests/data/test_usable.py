import src.data.usable as usable

import pytest


class TestUsable:

    @pytest.fixture
    def dataset(self):
        data, fields, labels = usable.Usable().summary()
        return data, fields, labels

    def test_instances(self, dataset):
        inventory, fields, labels = dataset
        summary = usable.Usable().instances(inventory, labels)
        assert summary.sum() == inventory[labels].sum(axis=0).sum()

    def test_summary(self, dataset):
        inventory, fields, labels = dataset

        assert len(labels) != 0, "At least one label column must exist"
        assert len(fields) != 0, "Missing field names"
        assert inventory.image.unique().shape[0] == inventory.shape[0], "Each image name can occur once only"
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"
