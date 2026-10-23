"""
Reads config.xml and turns it into the two things we need for Redis:
  * one JSON array of all subdomains, and
  * one key/value pair per cookie element
"""

import json
import xml.etree.ElementTree as ET

SUBDOMAINS_KEY = "subdomains"
COOKIE_KEY_FORMAT = "cookie:%s:%s"


def parse_config(path):
    """Parse the XML file and return (subdomains, cookies).

    subdomains is a plain list of strings, cookies is a dict keyed by
    "cookie:%NAME%:%HOST%". Order of subdomains is kept as it appears
    in the file.
    """
    tree = ET.parse(path)
    root = tree.getroot()

    subdomains = []
    for element in root.find("subdomains").findall("subdomain"):
        # .text is None for <subdomain></subdomain>, skip those
        if element.text:
            subdomains.append(element.text.strip())

    # Dict keyed by the redis key, easier to compare in tests
    cookies = {}
    cookies_element = root.find("cookies")
    if cookies_element is not None:
        for cookie in cookies_element.findall("cookie"):
            name = cookie.get("name")
            host = cookie.get("host")
            key = COOKIE_KEY_FORMAT % (name, host)
            cookies[key] = (cookie.text or "").strip()

    return subdomains, cookies


def subdomains_json(subdomains):
    """Serialize the subdomain list the way we store it in Redis."""
    # json.dumps keeps the non-ascii characters escaped, acceptable
    # here because the values are urls
    return json.dumps(subdomains)