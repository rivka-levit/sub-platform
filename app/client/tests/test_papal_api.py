"""
Tests for PayPal app.
Command: pytest client\tests\test_papal_api.py
"""

from client.paypal import get_access_token


def test_access_token():
    access_token = get_access_token()

    assert type(access_token) is str
