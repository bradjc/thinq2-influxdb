Thinq2 to InfluxDB 1.x
======================

This tool listens for Thinq2 messages and pushes them to an InfluxDB 1.x
database.

I've only tried this with an LG washing machine.

Setup
-----

First you need to get an oauth token.

```
git clone https://github.com/tinkerborg/thinq2-python
cd thinq2-python
poetry install
COUNTRY_CODE=US LANGUAGE_CODE=en-US poetry run python example.py
```

That will create `state.json`. Copy that file to this repo.

### Config Files

`/etc/swarm-gateway/influx-lgthinq.conf`:

```
url=
port=
username=
password=
database=
```

and

`/etc/swarm-gateway/lgthinq.conf`:

```
location_general=
```
