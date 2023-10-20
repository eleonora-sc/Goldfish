from ripe.atlas.cousteau import AtlasSource
from ripe.atlas.sagan import SslResult, TracerouteResult, Result, traceroute
from ripe.atlas.cousteau import ProbeRequest, Probe, AtlasResultsRequest, AtlasLatestRequest
import os
import requests
import geoip2.webservice

def get_lat_long(ip:str):
    with geoip2.webservice.Client(account_id=926113, license_key='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', host="geolite.info") as client:
        try:
            response = client.city(ip)
            # use logger for this instead
            print(f'GeoLite2: country:{response.country.name} - city:{response.city.name} - {response.location.latitude},{response.location.longitude}')
            return [response.location.latitude, response.location.longitude]

        except:
            # TODO use logger to log problem
            print('problem')
            return [None, None]

# unfortunately sagan is only fully compatible with v1 of the ripe atlas api
def get_traceroute_results(measurement_id):
    if not measurement_id:
        raise ValueError("Measurement ID is required")
    
    traceroute_json={}
    traceroute_json['measurement_id'] = measurement_id
    traceroute_json['source_probes'] = []
    print(traceroute_json)
    
    source = f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results/?format=json" # sagan documentation for this is deprecated, use: https://atlas.ripe.net/docs/apis/rest-api-reference/#measurements
    traceroute_result = requests.get(source)
    if traceroute_result.status_code == 200: # 200 means success
        traceroute_result_json = traceroute_result.json()

        for i, probe in enumerate(traceroute_result_json):
            traceroute_json['source_probes'].append({})
            probe_json = traceroute_json['source_probes'][i]
            # print(f'Probe {i}\n', probe, '\n')
            
            parsed_result = TracerouteResult(probe)

            # Traceroute attributes: https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html#traceroute 
            probe_json['probe_num'] = i+1
            probe_json['probe_id'] = parsed_result.probe_id
            probe_json['probe_ip'] = probe['src_addr'] # can't use Cousteau's Probe class because some probes aren't public
            probe_lat_long = get_lat_long(probe_json['probe_ip'])
            probe_json['probe_lat'] = probe_lat_long[0]
            probe_json['probe_long'] = probe_lat_long[1]

            # Testing if below attributes are necessary
            print("is_error:", parsed_result.is_error)
            print("is_malformed:", parsed_result.is_malformed)
            # print("protocol:", parsed_result.protocol)
            # print("ip_path:",parsed_result.ip_path)
            print("is_success:", parsed_result.is_success)
            print("destination_ip_responded:", parsed_result.destination_ip_responded)            
            
            probe_json['hops']=[]
            for j, hop in enumerate(parsed_result.hops):
                probe_json['hops'].append({})
                hops_json = probe_json['hops'][j]
                hops_json['hop_num'] = j+1

                # each hop contains (per default) a list of 3 packets
                if hop.packets[0]:
                    try:
                        hops_json['hop_ip'] = hop.packets[0].origin
                        hops_json['hop_rtt'] = hop.median_rtt
                        hop_lat_long = get_lat_long(hops_json['hop_ip'])
                        hops_json['hop_lat'] = hop_lat_long[0]
                        hops_json['hop_long'] = hop_lat_long[1]
                    except:
                        # use logger to 
                        hops_json['hop_ip'] = None
                        hops_json['hop_rtt'] = None
                        hops_json['hop_lat'] = None
                        hops_json['hop_long'] = None
                        print('packet empty')
                else:
                    print("   - No AS information available for this node")
            
            
        print(traceroute_json)

    else:
        raise Exception("HTTP request to API failed")
    
def parse_all_measurements():
    # TODO make this read the measurements.csv and iterate through the measurements
    pass

if __name__ == "__main__":
    get_traceroute_results(61984615)