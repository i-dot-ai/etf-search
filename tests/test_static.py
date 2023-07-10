from etf.jinja2 import static

from . import utils


@utils.with_client
def test_static(client):
    urls = (
        "dist/assets/index.js",
        "dist/assets/index.css",
        "i-dot-ai/images/crown.svg",
        "fonts/pxiByp8kv8JHgFVrLCz7Z1xlFd2JQEk.woff2",
    )
    for url in urls:
        response = client.get(static(url))
        assert response.status_code == 200, response.status_code
