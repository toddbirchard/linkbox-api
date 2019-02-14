import os
import json
import pprint
from datetime import datetime as dt
import requests
from flask import request, make_response, render_template


def sanitize_data(obj):
    """Sanitizes link embed data to be human-readable."""
    # Clean URL to be easily readable.
    displayurl = obj['url'].split('://')[0]
    displayurl = displayurl.replace('www.', '')
    obj['displayurl'] = displayurl
    # Reformat date
    published = dt.strftime(obj['publishDate'], '%m/%d/%Y %p')
    obj['publishDate'] = published
    # Format tags
    tags = [lambda x: '#' + x.replace(' ', ''), obj['tags']]
    obj['tags'] = tags
    return obj


def get_aylien_extract(url):
    """Extract url information using aylien API."""
    headers = {
        'X-AYLIEN-TextAPI-Application-Key': os.environ.get('AYLIEN_APP_KEY'),
        'X-AYLIEN-TextAPI-Application-ID': os.environ.get('AYLIEN_APP_ID'),
        'Content-Type': 'application/json'
    }
    params = {
        'url': url,
        'best_image': 'true'
    }
    base_url = 'https://api.aylien.com/api/v1/extract'
    req = requests.get(base_url, headers=headers, params=params)
    return req.json()


def get_aylien_summary(url):
    """Generate a 3-sentence summary of the URL using Aylien."""
    headers = {
        'X-AYLIEN-TextAPI-Application-Key': os.environ.get('AYLIEN_APP_KEY'),
        'X-AYLIEN-TextAPI-Application-ID': os.environ.get('AYLIEN_APP_ID')
    }
    params = {
        'url': url,
        'sentences_number': 3
    }
    base_url = 'https://api.aylien.com/api/v1/summarize'
    req = requests.get(base_url, headers=headers, params=params)
    sentences = req.json()['sentences']
    summary = ' '.join(sentences)
    return summary


def make_preview(linkpreview):
    """Create post preview HTML from link preview JSON."""
    if linkpreview is not None:
        return render_template('linkpreview.html', data=linkpreview)
    return None


def generate_url_metadata(url):
    """Create link preview metadata object.

    1. Create extract using Aylien Extract API.
    2. Generate URL summary using Aylien Summary API.
    3. Add simple metadata to object.
    4. Sanitize data.
    65 Return embed object.
    """
    preview_obj = get_aylien_extract(url)
    summary = get_aylien_summary(url)
    preview_obj['summary'] = summary
    preview_obj['url'] = url
    preview_obj.pop('article', None)
    preview_obj = sanitize_data(preview_obj)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(preview_obj)
    return preview_obj
