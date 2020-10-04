# type: ignore

from .. import webapp


def test_config():
    """Test create_app without passing test config."""
    assert not webapp.create_app().testing
    assert webapp.create_app({"TESTING": True}).testing
