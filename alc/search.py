from urllib.parse import quote

import requests
from lxml import html

from .path import CACHE_ROOT

_CACHE_DIR = CACHE_ROOT / 'search'


def _as_query(input_text):
    return '+'.join(quote(word.encode()) for word in input_text.split())


def _as_cache_path(input_text):
    return _CACHE_DIR / (_as_query(input_text) + '.html')


def _search(input_text):
    response = requests.request(
        'GET', 'http://eow.alc.co.jp/search?q={q}'.format(
            q=_as_query(input_text)))

    dom = html.fromstring(response.text)
    results_list = dom.xpath('//div[@id="resultsList"]')

    assert len(results_list) <= 1

    if not results_list:
        return html.fromstring('<br>')
    else:
        return results_list[0]


def search(input_text):
    cache_path = _as_cache_path(input_text)

    try:
        with open(cache_path, encoding='utf-8') as fh:
            results_list = html.fromstring(fh.read())
    except (FileNotFoundError, ValueError):
        results_list = _search(input_text)

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'wb') as fh:
            fh.write(html.tostring(results_list, encoding='utf-8'))

    return results_list
