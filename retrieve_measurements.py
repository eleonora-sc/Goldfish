"""
Intended use: retrieve a traceroute or ping measurement result and prepare it for visualization
(1) Retrieve the result using retrieve_traceroute_measurement/retrieve_ping_measurement, which makes use of the RipeAtlasMeasurements class method get_measurement_result
(2) Format it by deleting unneccessary elements using format_traceroute_result/format_ping_result
(3) If traceroute measurement, find latitudes and longitudes for traceroute hops using attach_lat_long



"""

from GMeasurements.measurements import RipeAtlasMeasurements
import json
from requests import get
from datetime import datetime

def get_geolocation_info(ip):
    response = get(f"http://ip-api.com/json/{ip}?fields=status,message,countryCode,city,lat,lon,isp,reverse,hosting")
    print(response)
    # if we do more than 45 requests per minute, 429 too many requests is returned
    if response.status_code == 200:
        return response.json()
    else:
        return False



def format_traceroute_result(result:list):
    formatted_result = [] # list of probes used in this measurement

    # for each probe used, format the result
    for probe in result:
        new_probe = {} # 1
        new_probe["msm_id"] = probe["msm_id"] # unchanged, measurement id
        new_probe["prb_id"] = probe["prb_id"] # unchanged, probe id
        new_probe["src_addr"] = probe["from"] # using probe["from"] instead of probe["src_addr"] since probe["src_addr"] is always the private ip
        new_probe["src_info"] = {
            "src_lat" : -1,
            "src_long": -1,
            "src_country": "",
            "src_city": "",
            "src_isp": "",
            "src_reverse": "",
            "src_hosting": False
        }
        new_probe["dst_addr"] = probe["dst_addr"] # unchanged
        new_probe["dst_info"] = {
            "dst_lat" : -1,
            "dst_long": -1,
            "dst_country": "",
            "dst_city": "",
            "dst_isp": "",
            "dst_reverse": "",
            "dst_hosting": False
        }

        # get geolocation info for the source and add it to new_probe["src_info"] if geolocation was successful
        src_geo_info = get_geolocation_info(new_probe["src_addr"])
        if src_geo_info and src_geo_info["status"] == "success":
            new_probe["src_info"]["src_lat"] = src_geo_info["lat"]
            new_probe["src_info"]["src_long"] = src_geo_info["lon"]
            new_probe["src_info"]["src_country"] = src_geo_info["countryCode"]
            new_probe["src_info"]["src_city"] = src_geo_info["city"]
            new_probe["src_info"]["src_isp"] = src_geo_info["isp"]
            new_probe["src_info"]["src_reverse"] = src_geo_info["reverse"]
            new_probe["src_info"]["src_hosting"] = src_geo_info["hosting"]

        # get geolocation info for the destination and add it to new_probe["dst_info"] if geolocation was successful
        dst_geo_info = get_geolocation_info(new_probe["dst_addr"])
        if dst_geo_info and dst_geo_info["status"] == "success":
            new_probe["dst_info"]["dst_lat"] = dst_geo_info["lat"]
            new_probe["dst_info"]["dst_long"] = dst_geo_info["lon"]
            new_probe["dst_info"]["dst_country"] = dst_geo_info["countryCode"]
            new_probe["dst_info"]["dst_city"] = dst_geo_info["city"]
            new_probe["dst_info"]["dst_isp"] = dst_geo_info["isp"]
            new_probe["dst_info"]["dst_reverse"] = dst_geo_info["reverse"]
            new_probe["dst_info"]["dst_hosting"] = dst_geo_info["hosting"]

        # clean up hop data
        new_probe_result = [] # 2

        for hop in probe["result"]:
            new_hop = {} # 3
            new_hop["hop"] = hop["hop"] # unchanged, hop number
            new_hop["from"] = "x" # added, ip address of hop
            new_hop["hop_info"] = {
                "hop_lat" : -1,
                "hop_long": -1,
                "hop_country": "",
                "hop_city": "",
                "hop_isp": "",
                "hop_reverse": "",
                "hop_hosting": False
            }
            new_hop["avg_rtt"] = -1 # added, averaging the (up to) 3 rtts of the (up to) 3 successful packets sent each hop

            # if at least one of the three packets returned a successful response, get ip address of hop and rtts of hop
            if not ("x" in hop["result"][0] and "x" in hop["result"][1] and "x" in hop["result"][2]):
                rtts = [] # create a variable to store up to 3 rtts from the 3 packets
                for packet in hop["result"]:
                    # if this packet was successful, get ip and rtt
                    if not "x" in packet:
                        new_hop["from"] = packet["from"]

                        rtts.append(packet["rtt"])

                # if ip is not x (meaning no packet was successful), get geolocation
                if new_hop["from"] != "x":
                    hop_geo_info = get_geolocation_info(new_hop["from"])
                    if hop_geo_info and hop_geo_info["status"] == "success":
                        new_hop["hop_info"]["hop_lat"] = hop_geo_info["lat"]
                        new_hop["hop_info"]["hop_long"] = hop_geo_info["lon"]
                        new_hop["hop_info"]["hop_country"] = hop_geo_info["countryCode"]
                        new_hop["hop_info"]["hop_city"] = hop_geo_info["city"]
                        new_hop["hop_info"]["hop_isp"] = hop_geo_info["isp"]
                        new_hop["hop_info"]["hop_reverse"] = hop_geo_info["reverse"]
                        new_hop["hop_info"]["hop_hosting"] = hop_geo_info["hosting"]

                
                # getting average rtt of all the successful packets' rtts
                if not len(rtts) == 0:
                    new_hop["avg_rtt"] = sum(rtts)/len(rtts)         

            new_probe_result.append(new_hop) # end 3 - add hop dict to new_probe_result list 


        # add new hop data to new_probe["result"]
        new_probe["result"] = new_probe_result # end 2
        
        # add new probe data to formatted_result["result"]
        formatted_result.append(new_probe) # end 1 - add new probe dict to formatted_result list
        break


    return formatted_result


def format_ping_result(result:list):
    formatted_result = []
    
    for measurement in result:
        new_measurement = {}
        new_measurement["msm_id"] = measurement["msm_id"]
        new_measurement["prb_id"] = measurement["prb_id"]
        new_measurement["src_addr"] = measurement["src_addr"]
        new_measurement["from"] = measurement["from"]
        new_measurement["dst_addr"] = measurement["dst_addr"]
        new_measurement["avg"] = measurement["avg"]
        new_measurement["timestamp"] = str(datetime.fromtimestamp(measurement["timestamp"]))
        new_measurement["stored_timestamp"] = str(datetime.fromtimestamp(measurement["stored_timestamp"]))


    
        formatted_result.append(new_measurement)
    
    return formatted_result

def retrieve_traceroute_measurement(msm_id): # ONLY WORKS FOR ONE-OFF TRACEROUTE MEASUREMENTS
    measurement = RipeAtlasMeasurements()
    retrieved_measurement = measurement.get_measurement_result(str(msm_id))

    formatted_measurement = format_traceroute_result(result=retrieved_measurement)

    with open(file=f"data/measurement_results/traceroute-{msm_id}.json", mode='w') as f:
        json.dump(formatted_measurement, f, indent=4)


def retrieve_ping_measurement(msm_id): # WORKS FOR BOTH ONE-OFF AND ONGOING PING MEASUREMENTS
    measurement = RipeAtlasMeasurements()
    retrieved_measurement = measurement.get_measurement_result(str(msm_id))

    formatted_measurement = format_ping_result(result=retrieved_measurement)

    with open(file=f"data/measurement_results/ping-{msm_id}.json", mode='w') as f:
        json.dump(formatted_measurement, f, indent=4)



if __name__ == "__main__":
    traceroute_old_msm_ids = [61984619, 61984618, 61984617, 61984615,61984614]
    traceroute_new_msm_ids = []
    ping_old_ongoing_msm_ids = [63466931,63466932,63466933,63466934,63466935,63466936,63466937,63466938,63466939,63466940]
    ping_new_ongoing_msm_ids = []

    # retrieve_traceroute_measurement(traceroute_msm_ids[0])
    retrieve_ping_measurement(ping_old_ongoing_msm_ids[1])
