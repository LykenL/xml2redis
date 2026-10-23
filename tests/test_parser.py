import json
import xml.etree.ElementTree as ET

import pytest

from app.parser import parse_config, subdomains_json


def test_parses_all_subdomains(real_config):
    subdomains, _ = real_config
    assert len(subdomains) == 38
    # first and last one, the list is in file order
    assert subdomains[0] == "http://secureline.tools.avast.com"
    assert subdomains[37] == "https://bits.avcdn.net"


def test_parses_all_cookies(real_config):
    _, cookies = real_config
    # 23 avast + 23 avg
    assert len(cookies) == 46


def test_cookie_keys_use_name_and_host(real_config):
    _, cookies = real_config
    assert cookies["cookie:dlp-avast:amazon"] == "mmm_amz_dlp_777_ppc_m"
    assert cookies["cookie:dlp-avg:vector"] == "mmm_vct_dlp_779_ppc_m"


def test_subdomains_json_is_a_valid_array(real_config):
    subdomains, _ = real_config
    payload = subdomains_json(subdomains)
    assert json.loads(payload) == subdomains
    assert payload.startswith('["http://')


def test_parses_minimal_file(minimal_path):
    subdomains, cookies = parse_config(minimal_path)
    assert len(subdomains) == 2
    assert cookies["cookie:dlp-avg:amazon"] == "mmm_amz_dlp_779_ppc_m"


def test_malformed_xml_raises_parse_error():
    path = __import__("os").path.join(
        __import__("os").path.dirname(__file__), "fixtures", "broken.xml"
    )
    with pytest.raises(ET.ParseError):
        parse_config(path)
