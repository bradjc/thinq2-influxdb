#!/usr/bin/env python3

import json
import os
import sys

import influxdb
import thinq2.controller.thinq


STATE_FILE = "state.json"


CONFIG_FILE_PATH = "/etc/swarm-gateway/lgthinq.conf"
INFLUX_CONFIG_FILE_PATH = "/etc/swarm-gateway/influx-lgthinq.conf"

# Get LG thinq2 config.
lg_config = {}
with open(CONFIG_FILE_PATH) as f:
    for l in f:
        fields = l.split("=")
        if len(fields) == 2:
            lg_config[fields[0].strip()] = fields[1].strip()

# Get influxDB config.
influx_config = {}
with open(INFLUX_CONFIG_FILE_PATH) as f:
    for l in f:
        fields = l.split("=")
        if len(fields) == 2:
            influx_config[fields[0].strip()] = fields[1].strip()


if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        thinq = thinq2.controller.thinq.ThinQ(json.load(f))
else:
    print("Need to create state.json using the thinq2-python library.")
    sys.exit(-1)


tags = {}


influx_client = influxdb.InfluxDBClient(
    influx_config["url"],
    influx_config["port"],
    influx_config["username"],
    influx_config["password"],
    influx_config["database"],
    ssl=True,
    gzip=True,
    verify_ssl=True,
)


def handle_mqtt_message(client, userdata, msg):
    print(msg.payload)
    s = msg.payload.decode("utf-8")
    pkt = json.loads(s)

    try:
        # All see to have the following two sections. If not just skip this one.
        device_id = pkt["deviceId"]
        report = pkt["data"]["state"]["reported"]

        # If no meta data, fetch now.
        if not device_id in tags:
            device = thinq.mqtt.thinq_client.get_device(device_id)

            tags[device_id] = {
                "device_id": device_id,
                "model": device.model_name,
                "alias": device.alias,
                "mac_address": device.mac_address,
                "user_no": device.user_no,
                "model_protocol": device.model_protocol,
                "location_general": lg_config["location_general"],
            }

        wd = report["washerDryer"]

        # print(wd)

        point = {
            "measurement": "lg_washer",
            "fields": wd,
            "tags": tags[device_id],
        }

        print(point)

        influx_client.write_points([point])

    except:
        print("Could not parse:")
        print(pkt)
        pass


thinq.mqtt.on_message = handle_mqtt_message
thinq.mqtt.connect()

print("Listening for events from Thinq2...")

thinq.mqtt.loop_forever()
