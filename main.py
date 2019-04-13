import json
from flask import make_response, request
from endpoint import fetch


def scrape(request):
    """Scrape scheduled link previews.

    1. Extarct target URL from query string.
    2. Call get_meta constructor.
    3. Convert metadata to JSON object.
    4. Return response.
    """
    target_url = request.args.get('url')
    previews = fetch.get_meta(target_url)
    response_body = json.dumps(previews)
    return make_response(str(response_body), 200)
