# type: ignore

from unittest.mock import MagicMock

from .. import webapp

import spotipy


def test_config():
    """
    Test create_app with different configs.
    """
    dev_app = testing_app = webapp.create_app()

    assert not dev_app.testing
    assert isinstance(dev_app.spotify, spotipy.Spotify)

    testing_app = webapp.create_app({"TESTING": True})

    assert testing_app.testing
    assert isinstance(testing_app.spotify, MagicMock)
