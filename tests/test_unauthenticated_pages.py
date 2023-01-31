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
    assert response.status_code == 302


@with_client
def test_get_my_evaluations(client):
    response = client.get("/my-evaluations/")
    assert response.status_code == 302


@with_client
def test_get_login(client):
    response = client.get("/accounts/login/")
    assert response.status_code == 200
