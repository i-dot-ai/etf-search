import functools

import httpx

import etf.wsgi

TEST_SERVER_URL = "http://etf-testserver:8010/"


def with_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        with httpx.Client(app=etf.wsgi.application, base_url=TEST_SERVER_URL) as client:
            return func(client, *args, **kwargs)

    return _inner


@with_client
def test_add_evaluation(client):
    response = client.get("/")
    assert response.status_code == 200
