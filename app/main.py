"""
Command line entry point:

    python -m app.main config.xml        # export only
    python -m app.main -v config.xml     # export, then print the keys
"""

import argparse
import sys

import redis

from app.parser import SUBDOMAINS_KEY, parse_config, subdomains_json

DEFAULT_REDIS_URL = "redis://localhost:6379/0"


def export(path, redis_url):
    """Write the parsed data into Redis and return the client."""
    subdomains, cookies = parse_config(path)

    client = redis.Redis.from_url(redis_url)

    # one key with the whole list as JSON
    client.set(SUBDOMAINS_KEY, subdomains_json(subdomains))

    for key, value in cookies.items():
        client.set(key, value)

    return client, len(cookies) + 1


def print_keys(client):
    """Print every key we saved, with the value next to it."""
    keys = sorted(client.keys("cookie:*")) + [SUBDOMAINS_KEY.encode()]

    print("Keys in Redis:")
    for key in keys:
        print("  %s = %s" % (key.decode(), client.get(key).decode()))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export config.xml into Redis")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print all keys saved to Redis")
    parser.add_argument("xml", help="path to the xml file")
    parser.add_argument("--redis-url", default=DEFAULT_REDIS_URL,
                        help="redis connection url")
    args = parser.parse_args(argv)

    try:
        client, count = export(args.xml, args.redis_url)
    except FileNotFoundError:
        print("error: cannot find %s" % args.xml, file=sys.stderr)
        return 1
    except redis.ConnectionError:
        print("error: cannot reach Redis at %s" % args.redis_url, file=sys.stderr)
        return 1

    print("Exported %d keys to Redis" % count)

    if args.verbose:
        print_keys(client)

    return 0


if __name__ == "__main__":
    sys.exit(main())