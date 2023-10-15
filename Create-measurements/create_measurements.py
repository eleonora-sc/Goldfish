from ripe.atlas.cousteau import AtlasSource, AtlasCreateRequest, Ping, Traceroute, Probe
from ripe.atlas.sagan import SslResult
import os
from dotenv import load_dotenv
from datetime import datetime

def load_api_key():
    load_dotenv()
    ATLAS_API_KEY = os.getenv('ATLAS_API_KEY')
    
    return ATLAS_API_KEY

# Ping measurements
def create_ping_measurements():
    targets = [{"GCI", "vcns-3.gci.net"}, {"ACS", "209.193.4.7"}]

# Traceroute Measurements
def create_traceroute_measurements(targets:list, sources:str, ATLAS_API_KEY:str):
    for i, target in enumerate(targets):
        print(f"trying target {i}, with target {target}")
        traceroute = Traceroute(
            af=4,
            target = target,
            description = f"Goldfish OFFICIAL traceroute measurement {i+1} to {target}",
            protocol="ICMP",
        )
        source = AtlasSource(
            type="probes",
            value=sources, # must be in this format
            requested=1,
            tags={"include":["system-ipv4-works"]},
        )
        atlas_request = AtlasCreateRequest(
            start_time=datetime.utcnow(),
            key=ATLAS_API_KEY,
            measurements=[traceroute],
            sources=[source],
            is_oneoff=True
        )

        (is_success, response) = atlas_request.create()
        print(is_success)
        print(response)
        # instead of printing, need to append sources string, target ip string, and response['measurements'][0]to measurements.csv

def find_target_probe_ips(traceroute_targets:list):
    target_ips = []
    for i, target in enumerate(traceroute_targets):
        probe = Probe(id=target)
        target_ips.append(probe.address_v4)
        print(f"{probe.country_code} - {probe.address_v4}")

    return target_ips




if __name__ == "__main__":
    ATLAS_API_KEY = load_api_key()
    # list of active probes in Alaska in key value pairs of id, description
    alaska_nodes = {14300: "Juneau", 51310: "Anchorage 2", 51754: "Anchorage 3", 52344: "Eagle River", 60259: "Anchorage 4", 61113: "Palmer", 61868: "Anchorage 1"}
    alaska_nodes_string = "14300,52344,61868,61113"

    # list of targets for traceroute measurements in key value pairs
    traceroute_targets = {62796: "Lagos", 1004023: "Rio", 1005456: "New Delhi", 1006001: "Berlin", 1002558: "Sydney"}
    traceroute_target_ips =  find_target_probe_ips([key for key in traceroute_targets])

    create_traceroute_measurements(traceroute_target_ips, alaska_nodes_string, ATLAS_API_KEY)