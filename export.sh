#!/usr/bin/env bash
#
# Usage: ./export.sh [-v] /path/to/xml
#
# Starts the redis container if needed and runs the export inside the app
# container. The xml file is mounted into the container read only.

set -e

XML=""
VERBOSE=""

while getopts "v" opt; do
    case "$opt" in
        v) VERBOSE="1" ;;
        *) echo "usage: $0 [-v] /path/to/xml" >&2; exit 2 ;;
    esac
done
shift $((OPTIND - 1))

XML="$1"

if [ -z "$XML" ]; then
    echo "usage: $0 [-v] /path/to/xml" >&2
    exit 2
fi

if [ ! -f "$XML" ]; then
    echo "error: no such file: $XML" >&2
    exit 1
fi

# absolute path, docker compose needs one for the volume
XML="$(cd "$(dirname "$XML")" && pwd)/$(basename "$XML")"

cd "$(dirname "$0")"

docker compose up -d redis

ARGS="-v /data/config.xml"
if [ -n "$VERBOSE" ]; then
    ARGS="-v $ARGS"
fi

docker compose run --rm -v "$XML:/data/config.xml:ro" app python -m app.main $ARGS
