"""
Intended use: retrieve a traceroute or ping measurement result and prepare it for visualization
(1) Retrieve the result using retrieve_traceroute_measurement/retrieve_ping_measurement, which makes use of the RipeAtlasMeasurements class method get_measurement_result
(2) Format it by deleting unneccessary elements using format_traceroute_result/format_ping_result
(3) If traceroute measurement, find latitudes and longitudes for traceroute hops using attach_lat_long



"""

from GMeasurements.measurements import RipeAtlasMeasurements
import json

def format_traceroute_result(result:list):
    formatted_result = [] # list of probes used in this measurement
    
    # for each probe used, format the result
    for probe in result:
        new_probe = {} # 1
        new_probe["msm_id"] = probe["msm_id"] # unchanged, measurement id
        new_probe["prb_id"] = probe["prb_id"] # unchanged, probe id
        new_probe["src_addr"] = probe["from"] # using probe["from"] instead of probe["src_addr"] since probe["src_addr"] is always the private ip
        new_probe["src_lat"] = -1 # added
        new_probe["src_long"] = -1 # added
        new_probe["dst_addr"] = probe["dst_addr"] # unchanged
        new_probe["dst_lat"] = -1 # added
        new_probe["dst_long"] = -1 # added


        # TODO get latlongs for new_probe["src_addr"] and new_probe["dst_addr"], which are the source and destination addresses as a string


        # clean up hop data
        new_probe_result = [] # 2

        for hop in probe["result"]:
            new_hop = {} # 3
            new_hop["hop"] = hop["hop"] # unchanged, hop number
            new_hop["from"] = "x" # added, ip address of hop
            new_hop["lat"] = -1 # added, latitude of hop
            new_hop["long"] = -1 # added, longitude of hop
            new_hop["avg_rtt"] = -1 # added, averaging the (up to) 3 rtts of the (up to) 3 successful packets sent each hop

            # if at least one of the three packets returned a successful response, get ip address of hop and rtts of hop
            if not ("x" in hop["result"][0] and "x" in hop["result"][1] and "x" in hop["result"][2]):
                rtts = [] # create a variable to store up to 3 rtts from the 3 packets
                for packet in hop["result"]:
                    # if this packet was successful, get ip and rtt
                    if not "x" in packet:
                        new_hop["from"] = packet["from"]


                        # TODO we need the latlongs of new_hop["from"], which is the ip address as a string


                        rtts.append(packet["rtt"])
                
                # getting average rtt of all the successful packets' rtts
                new_hop["avg_rtt"] = sum(rtts)/len(rtts)         

            new_probe_result.append(new_hop) # end 3 - add hop dict to new_probe_result list 


        # add new hop data to new_probe["result"]
        new_probe["result"] = new_probe_result # end 2
        
        # add new probe data to formatted_result["result"]
        formatted_result.append(new_probe) # end 1 - add new probe dict to formatted_result list


    return formatted_result


def retrieve_traceroute_measurement(msm_id):
    measurement = RipeAtlasMeasurements()
    retrieved_measurement = measurement.get_measurement_result(str(msm_id))

    formatted_measurement = format_traceroute_result(result=retrieved_measurement)

    with open(file=f"data/measurement_results/{msm_id}.json", mode='w') as f:
        json.dump(formatted_measurement, f, indent=4)

    # print(retrieved_measurement)

if __name__ == "__main__":
    traceroute_msm_ids = [61984619, 61984618, 61984617, 61984615,61984614]
    retrieve_traceroute_measurement(traceroute_msm_ids[0])