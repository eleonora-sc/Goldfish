from ripe.atlas.cousteau import AtlasSource
from ripe.atlas.sagan import SslResult, TracerouteResult
from ripe.atlas.cousteau import ProbeRequest, Probe
import os
import requests

def testing_ripe_atlas_tools(): # testing done, deprecated
    # find all the probes in Alaska (lists the canada one too, just discard)
    os.system('wsl -e sh -c "ripe-atlas probe-search --status 1 --center=61.217,-149.863 --radius 1300 > alaska_probes.txt"') # latlong of anchorage, radius of 1500 km
    # os.system('wsl -e sh -c "ripe-atlas probe-search --area anchorage --status 1 > test.txt')


def get_traceroute_results():
    source = "https://atlas.ripe.net/api/v2/measurements/61840521/results/" # sagan documentation for this is deprecated, use: https://atlas.ripe.net/docs/apis/rest-api-reference/#measurements
    traceroute_result = requests.get(source)
    if traceroute_result.status_code == 200: # 200 means success
        traceroute_result_json = traceroute_result.json()

        parsed_result = TracerouteResult(traceroute_result_json)

        print("Measurement ID:", parsed_result.measurement_id)
        print("Probe ID:", parsed_result.probe_id)
        print("Timestamp:", parsed_result.timestamp)
        print("Hops:")
        for hop in parsed_result.hops:
            print("  Hop:")
            for packet in hop.packets:
                print("    - IP:", packet.ip)
                print("    - RTT:", packet.rtt)
        

        # Traceroute attributes: https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#traceroute 



    else:
        raise Exception("HTTP request to API failed")


if __name__ == "__main__":
    get_traceroute_results()