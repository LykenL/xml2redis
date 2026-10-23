# xml2redis

Exports the data from an XML config file into Redis.

## What goes into Redis

| Key | Value |
| --- | --- |
| `subdomains` | JSON array of all `<subdomain>` values |
| `cookie:<name>:<host>` | text of the `<cookie>` element |

For example, the element

    <cookie name="dlp-avast" host="amazon">mmm_amz_dlp_777_ppc_m</cookie>

is stored as `cookie:dlp-avast:amazon` = `mmm_amz_dlp_777_ppc_m`.

## Run it

    docker compose build
    docker compose up -d redis
    ./export.sh /path/to/config.xml

Add `-v` to print every key that was saved:

    ./export.sh -v /path/to/config.xml

The xml is mounted into the container, so any file on the host works.

## Tests

    pip install -r requirements-dev.txt 
    pytest # expected: 9 passed

The parser tests run anywhere. The export tests need a Redis on
`localhost:6379` and are skipped if there is none, so start the container
first if you want them to run.

## Layout

    app/parser.py   reads the xml
    app/main.py     writes to redis, command line
    export.sh       docker wrapper
    tests/          unit tests

