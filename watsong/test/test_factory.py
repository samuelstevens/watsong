# type: ignore


from .. import webapp


def test_config():
    """
    Test create_app with different configs.
    """
    dev_app = testing_app = webapp.create_app()

    assert not dev_app.testing

    testing_app = webapp.create_app({"TESTING": True})

    assert testing_app.testing
