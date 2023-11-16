from GMeasurements.measurements import RipeAtlasMeasurements, Payload
from dotenv import load_dotenv
from os import getenv
import json
import csv
from datetime import datetime

# TEST MEASUREMENTS
def test_oneoff_ping(auth_key):
    # create an instance of class RipeAtlasMeasurement that can be used for a lot of different measurements
    measurement = RipeAtlasMeasurements(ATLAS_API_KEY=auth_key)

    seattle_anchor_id = 7221
    new_payload = Payload()

    ping_params = {
    "target": "66.58.251.1",  # Target IP address or hostname to ping
    "description": "testing jaren's ripe atlas api wrapper, pinging 66.58.251.1",
    "af": 4,  # Address family, 4 for IPv4, 6 for IPv6
    "type": "ping",
    "packets": 3,  # Number of ping packets to send
    "size": 48,  # Size of the ping packets
    "packet_interval": 1000,  # Interval between packets in milliseconds
    "include_probe_id": True,  # Whether to include the probe ID in the ping
    "is_oneoff": True,  # If this is a one-time measurement
    }

    # Add the ping definition to your payload
    new_payload.add_ping_definition(**ping_params)

    # Define your probe parameters
    probe_params = {
        "requested": 1,  # Number of probes you request for the measurement
        "type": "probes",  # Type of the probe query (area, country, probes, etc.)
        "value": "7221"  # Area, country code, or list of probes 
    }

    # Add the probe to your payload
    new_payload.add_probe(**probe_params)

    # Create the measurement
    new_measurement = measurement.create_measurement("ping", new_payload)

    
    print(new_measurement)
    
    # appends measurement ids to this csv
    with open("data/measurements/test_measurements.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        for measurement in new_measurement:
            writer.writerow([measurement])


def test_ongoing_ping(auth_key):
    # create an instance of class RipeAtlasMeasurement that can be used for a lot of different measurements
    measurement = RipeAtlasMeasurements(ATLAS_API_KEY=auth_key)

    seattle_anchor_id = 7221
    new_payload = Payload()

    ping_params = {
    "target": "66.58.251.1",  # Target IP address or hostname to ping
    "description": "testing jaren's ripe atlas api wrapper, pinging 66.58.251.1",
    "af": 4,  # Address family, 4 for IPv4, 6 for IPv6
    "type": "ping",
    "packets": 3,  # Number of ping packets to send
    "size": 48,  # Size of the ping packets
    "packet_interval": 1000,  # Interval between packets in milliseconds
    "include_probe_id": True,  # Whether to include the probe ID in the ping
    "is_oneoff": False,  # If this is a one-time measurement
    "start_time":int(datetime(2023,11,9,20,55).timestamp()),
    "stop_time":int(datetime(2023,11,9,20,58).timestamp()),
    "interval": 60
    }

    # Add the ping definition to your payload
    new_payload.add_ping_definition(**ping_params)

    # Define your probe parameters
    probe_params = {
        "requested": 1,  # Number of probes you request for the measurement
        "type": "probes",  # Type of the probe query (area, country, probes, etc.)
        "value": "7221"  # Area, country code, or list of probes
    }

    # Add the probe to your payload
    new_payload.add_probe(**probe_params)

    # Create the measurement
    new_measurement = measurement.create_measurement("ping", new_payload)

    
    print(new_measurement)
    
    # appends measurement ids to this csv
    with open("data/measurements/test_measurements.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        for measurement in new_measurement:
            writer.writerow([measurement])


# OFFICIAL MEASUREMENTS
def create_ongoing_ping(auth_key): 
    # create an instance of class RipeAtlasMeasurement that can be used for a lot of different measurements
    measurement = RipeAtlasMeasurements(ATLAS_API_KEY=auth_key)

    new_payload = Payload()

    remote_target_list = [
        {"Kotzebue 1": "216.163.106.1"}, 
        {"Kotzebue 2": "74.127.92.1"},
        {"Nome":"67.59.96.3"},
        {"Bethel": "24.237.58.1"},
        {"Alakanuk": "67.58.30.2"}, # not sure
        {"Metlakatla":"64.186.125.1"},
        {"Dillingham":"107.152.126.1"}, # not sure
        {"Chevak":"24.237.232.2"}, # not sure
        {"Unalaska":"172.87.239.1"},
        {"Nunapitchuk":"66.58.251.1"},
        {"Utqiagvik":"24.237.124.4"} # not sure
        ]
    
    # these are the comparison targets 
    compare_target_list = [
        {"Anchorage 1":"198.51.13.5"},
        {"Anchorage 2": "154.6.93.149"},
        {"Fairbanks 1": "199.165.82.221"},
        {"Fairbanks 2": "66.223.176.1"},
        {"Juneau 1": "192.245.44.0"},
        {"Juneau 2": "23.135.128.1"}
    ]
    
    for target in remote_target_list:
        (key, value), = target.items()
        ping_params = {
        "target": value,  # Target IP address or hostname to ping
        "description": f"PROJECT GOLDFISH - testing remote Alaska network, pinging {value} in {key} hourly",
        "af": 4,  # Address family, 4 for IPv4, 6 for IPv6
        "type": "ping",
        "packets": 3,  # Number of ping packets to send
        "size": 48,  # Size of the ping packets
        "packet_interval": 1000,  # Interval between packets in milliseconds
        "include_probe_id": True,  # Whether to include the probe ID in the ping
        "is_oneoff": False,  # If this is a one-time measurement
        "start_time":int(datetime(2023,11,15,15,30).timestamp()),
        "stop_time":int(datetime(2023,11,20,15,30).timestamp()),
        "interval": 3600
        }

        # Add the ping definition to your payload
        new_payload.add_ping_definition(**ping_params)
    
    for target in compare_target_list:
        (key, value), = target.items()
        ping_params = {
        "target": value,  # Target IP address or hostname to ping
        "description": f"PROJECT GOLDFISH - testing urban Alaska network for comparison with remote Alaska network, pinging {value} in {key} hourly",
        "af": 4,  # Address family, 4 for IPv4, 6 for IPv6
        "type": "ping",
        "packets": 3,  # Number of ping packets to send
        "size": 48,  # Size of the ping packets
        "packet_interval": 1000,  # Interval between packets in milliseconds
        "include_probe_id": True,  # Whether to include the probe ID in the ping
        "is_oneoff": False,  # If this is a one-time measurement
        "start_time":int(datetime(2023,11,15,15,30).timestamp()),
        "stop_time":int(datetime(2023,11,20,15,30).timestamp()),
        "interval": 3600
        }

        # Add the ping definition to your payload
        new_payload.add_ping_definition(**ping_params)

    seattle_anchor_id = 7221
    # Define your probe parameters
    probe_params = {
        "requested": 1,  # Number of probes you request for the measurement
        "type": "probes",  # Type of the probe query (area, country, probes, etc.)
        "value": f"{seattle_anchor_id}"  # Area, country code, or list of probes
    }

    # Add the probe to your payload
    new_payload.add_probe(**probe_params)

    # Create the measurement
    new_measurement = measurement.create_measurement("ping", new_payload)

    # appends measurement ids to this csv
    with open("data/measurements/ping_measurements.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        for measurement in new_measurement:
            writer.writerow([measurement])




if __name__ == "__main__":
    load_dotenv()
    auth_key = getenv("ATLAS_API_KEY","NONE")
    if auth_key == "None":
        raise("error getting atlas api key")
    
    # LATEST OFFICIAL MEASUREMENT
    create_ongoing_ping(auth_key=auth_key)


    
    