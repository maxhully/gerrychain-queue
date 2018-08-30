from unittest.mock import patch

from flask import Flask

from gerrychain_queue import create_app


@patch("gerrychain_queue.Flask")
def test_create_app_returns_an_app(MockFlask):
    MockFlask.return_value.__class__ = Flask
    app = create_app()
    assert isinstance(app, Flask)
