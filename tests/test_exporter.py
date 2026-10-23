import json
import os

import pytest
import redis

from app.main import export
from app.parser import SUBDOMAINS_KEY, subdomains_json

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


@pytest.fixture
def client():
    conn = redis.Redis.from_url(REDIS_URL)
    try:
        conn.ping()
    except redis.ConnectionError:
        pytest.skip("redis is not running, start it with docker compose up -d redis")

    conn.flushdb()
    yield conn
    conn.flushdb()


def test_export_writes_subdomains_key(client, config_path):
    export(config_path, REDIS_URL)

    raw = client.get(SUBDOMAINS_KEY)
    assert raw is not None

    subdomains = json.loads(raw)
    assert len(subdomains) == 38


def test_export_writes_cookie_keys(client, config_path):
    client, count = export(config_path, REDIS_URL)

    assert count == 47
    assert client.get("cookie:dlp-avast:amazon") == b"mmm_amz_dlp_777_ppc_m"
    assert client.get("cookie:dlp-avg:vector") == b"mmm_vct_dlp_779_ppc_m"


def test_running_twice_gives_same_result(client, config_path):
    export(config_path, REDIS_URL)
    first = sorted(client.keys("*"))

    export(config_path, REDIS_URL)
    second = sorted(client.keys("*"))

    assert first == second