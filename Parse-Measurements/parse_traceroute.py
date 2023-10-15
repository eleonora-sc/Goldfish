from ripe.atlas.cousteau import AtlasSource
from ripe.atlas.sagan import SslResult, TracerouteResult, Result, traceroute
from ripe.atlas.cousteau import ProbeRequest, Probe, AtlasResultsRequest, AtlasLatestRequest
import os
import requests

# unfortunately sagan is only fully compatible with v1 of the ripe atlas api
def get_traceroute_results():
    source = "https://atlas.ripe.net/api/v2/measurements/61984191/results/?format=json" # sagan documentation for this is deprecated, use: https://atlas.ripe.net/docs/apis/rest-api-reference/#measurements
    traceroute_result = requests.get(source)
    if traceroute_result.status_code == 200: # 200 means success
        traceroute_result_json = traceroute_result.json()

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
                print("   - median rtt:", hop.median_rtt)
                # print("    - packets:", hop.packets)  


                if hop.packets[0]:
                    try:
                        print("   - Probe IP:", hop.packets[0].origin)
                    except:
                        print('packet empty')
                        # raise Exception('packet empty')
                else:
                    print("   - No AS information available for this node")

    else:
        raise Exception("HTTP request to API failed")
    



if __name__ == "__main__":
    get_traceroute_results()