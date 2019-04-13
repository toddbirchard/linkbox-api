import requests
from bs4 import BeautifulSoup


def get_meta(url):
    """Generate preview obj per link.

    1. Set headers of outbound GET request.
    2. Determine title of target url.
    3. Create description blurb of target url.
    4. Find suitable image for target url.
    5. Determine the top-level site name of target url.
    6. Create dict of fetched metadata.
    7. Return result.
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    r = requests.get(url, headers=headers)
    embedded_link = BeautifulSoup(r.content, 'html.parser')
    preview_dict = {
        'title': get_title(embedded_link, url),
        'description': get_description(embedded_link),
        'image': get_image(embedded_link),
        'sitename': get_site_name(embedded_link, url),
        'url': url
        }
    return preview_dict


def get_site_name(link, url):
    """Attempt to get the site's base name.

    1. Check OG tags for site name.
    2. If no OG tag exists, get top-level domain from url.
    3. Return site name.
    """
    sitename = None
    if link.find("meta", property="og:site_name") is not None:
        sitename = link.find("meta", property="og:site_name").get('content')
    else:
        sitename = url.split('//')[1]
        name = sitename.split('/')[0]
        name = sitename.rsplit('.')[1]
        return name.capitalize()
    return sitename


def get_domain(url):
    """Get site root domain name."""
    domain = url.split('//')[1]
    name = domain.split('/')[0]
    return name


def get_title(link, url):
    """Attempt to get a title.

    1. Check metadata for title tag.
    2. If doesn't exist, check page for h1 tag.
    3. Remove all text which comes after the first pipe ("|") in the title.
    4. Return title.
    """
    title = url
    if link.title.string is not None:
        title = link.title.string
    elif link.find("h1") is not None:
        title = link.find("h1").string
    elif link.find_all("h1") is not None:
        title = link.find_all("h1")[0].string
    if title:
        title = title.split('|')[0]
    return title


def get_description(link):
    """Attempt to get description.

    1. Check OG tags for description tag.
    2. If doesn't exist, check page for p tag.
    3, Return description.
    """
    description = ""
    if link.find("meta", property="og:description") is not None:
        description = link.find("meta", property="og:description").get('content')
    elif link.find("p") is not None:
        description = link.find("p").contents
    elif link.find_all("p") is not None:
        description = link.find_all("p")[0].contents
    return description


def get_image(link):
    """Attempt to get image.

    1. Check OG tags for image tag.
    2. If doesn't exist, check page for img tag.
    3. If the image path is relative, make it absolute.
    4. Return image URL.
    """
    image = ""
    if link.find("meta", property="og:image") is not None:
        image = link.find("meta", property="og:image").get('content')
    elif link.find_all("img", src=True) is not None:
        image = link.find_all("img")
        if image:
            image = link.find_all("img")[0].get('src')
    if str(image)[0] == '/':
        image = str(get_domain(link)) + image
    return image


def site_exceptions(link, url):
    """Check to see if site is in list of exceptions."""
    domain = get_site_name(link, url)
    exception_domains = ['Youtube', 'Medium' 'Github']
    if domain in exception_domains:
        print('WARNING:', domain)
