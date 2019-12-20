import cfg.cfg as cfg
import src.data.sources as sources

variables = cfg.Cfg().variables()


class TestSources:

    def test_truth(self):
        truth_use = variables['source']['truth']['use']

        truth = sources.Sources().truth()
        assert truth.shape[0] != 0, "The ground truth labels file should not be empty"
        assert set(truth.columns) == set(truth_use), "The columns of truth must be those " \
                                                     "specified in variables.yml"

    def test_metadata(self):
        metadata_use = variables['source']['metadata']['use']

        metadata = sources.Sources().metadata()
        assert metadata.shape[0] != 0, "The metadata file should not be empty"
        assert set(metadata.columns) == set(metadata_use), "The columns of metadata must be those " \
                                                           "specified in variables.yml"

    def test_summary(self):
        truth_use = variables['source']['truth']['use']
        truth_key = variables['source']['truth']['key']
        metadata_use = variables['source']['metadata']['use']

        truth = sources.Sources().truth()
        metadata = sources.Sources().metadata()
        inventory, labels, fields = sources.Sources().summary()

        assert truth.shape[0] == inventory.shape[0], "The number of ground truth & inventory data points must be equal"
        assert metadata.shape[0] == inventory.shape[0], "The number of medata & inventory data points must be equal"

        assert set([truth_key] + labels) == set(truth_use), "The values of labels do not match the labels of truth"
        assert set(fields) == set(metadata_use), "A values of fields don't match the uploaded columns of metadata"

        assert inventory.image.unique().shape[0] == inventory.shape[0], "Each image name can occur once only"
        assert inventory[labels].sum(axis=1).all(), "Each image must be associated with a single class only"
