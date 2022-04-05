Thinq2 to InfluxDB 1.x
======================

This tool listens for Thinq2 messages and pushes them to an InfluxDB 1.x
database.

I've only tried this with an LG washing machine.

Setup
-----

First you need to get an oauth token.

```
sudo pip3 install poetry
git clone https://github.com/tinkerborg/thinq2-python
cd thinq2-python
poetry install
COUNTRY_CODE=US LANGUAGE_CODE=en-US poetry run python example.py
```

That will create `state.json`. Copy that file to this repo.

Then you need to install the thinq2 library after running `poetry install`:

```
sudo pip install git+https://github.com/tinkerborg/thinq2-python
```



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
device_id=
location_general=
```
