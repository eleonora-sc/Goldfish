from ripe.atlas.cousteau import AtlasSource
from ripe.atlas.sagan import SslResult, TracerouteResult, Result, traceroute
from ripe.atlas.cousteau import ProbeRequest, Probe, AtlasResultsRequest, AtlasLatestRequest
import os
import requests

def testing_ripe_atlas_tools(): # testing done, deprecated
    # find all the probes in Alaska (lists the canada one too, just discard)
    os.system('wsl -e sh -c "ripe-atlas probe-search --status 1 --center=61.217,-149.863 --radius 1300 > alaska_probes.txt"') # latlong of anchorage, radius of 1500 km
    # os.system('wsl -e sh -c "ripe-atlas probe-search --area anchorage --status 1 > test.txt')

# unfortunately sagan is only compatible with v1 of the ripe atlas api
def get_traceroute_results():
    source = "https://atlas.ripe.net/api/v2/measurements/61840521/results/?format=json" # sagan documentation for this is deprecated, use: https://atlas.ripe.net/docs/apis/rest-api-reference/#measurements
    traceroute_result = requests.get(source)
    if traceroute_result.status_code == 200: # 200 means success
        # print(traceroute_result.content) # bad, this is a byte object
        traceroute_result_json = traceroute_result.json()
        # print(traceroute_result_json)
        for i, probe in enumerate(traceroute_result_json):
            print(f'Probe {i}\n', probe, '\n')
            
            parsed_result = TracerouteResult(probe)

            # Traceroute attributes: https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#traceroute 
            print("Measurement ID:", parsed_result.measurement_id) # or 
            print("Source Probe ID:", parsed_result.probe_id)
            print("is_error:", parsed_result.is_error)
            print("is_malformed:", parsed_result.is_malformed)
            print("protocol:", parsed_result.protocol)
            print("ip_path:",parsed_result.ip_path)
            print("is_success:", parsed_result.is_success)
            print("destination_ip_responded:", parsed_result.destination_ip_responded)            # print("Timestamp:", parsed_result.)
            
            
            print("Hops:")
            for hop in parsed_result.hops:
                print("    Hop:", hop)
                print("    - median rtt:", hop.median_rtt)
                print("    - packets:", hop.packets)  
            # for hop in probe['result']:
            #     print(f"  Hop: {hop['hop']}\n")
            #     for packet in hop['result']:

                for packet in hop.packets:
                    if packet:
                        try:
                            print("   - Probe IP:", packet.origin)
                        except:
                            print('packet empty')
                            # raise Exception('packet empty')
                    else:
                        print("   - No AS information available for this node")



        
    else:
        raise Exception("HTTP request to API failed")
    



if __name__ == "__main__":
    get_traceroute_results()