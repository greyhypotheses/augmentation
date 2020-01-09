import src.data.images as images
import src.data.sources as sources


class TestImages:

    def test_states(self):
        listing, _, _ = sources.Sources().summary()
        states = images.Images().states(listing['image'])
        assert states.status.all(), "It seems one or more images do not exists in the repository.  " \
                                    "The missing images are listed in the logs."
