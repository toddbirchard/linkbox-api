from bs4 import BeautifulSoup
import pytest
import requests


@pytest.mark.parametrize("preview_url", 'https://google.com/')
def test_inspect_html(preview_url):
    """Inspect html of incoming page."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    r = requests.get(preview_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    assert True
    print(soup.prettify())


if __name__ == '__main__':
    pytest.main()
