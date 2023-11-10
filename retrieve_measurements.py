"""
Intended use: retrieve a traceroute or ping measurement result and prepare it for visualization
(1) Retrieve the result using retrieve_traceroute_measurement/retrieve_ping_measurement, which makes use of the RipeAtlasMeasurements class method get_measurement_result
(2) Format it by deleting unneccessary elements using format_traceroute_result/format_ping_result
(3) If traceroute measurement, find latitudes and longitudes for traceroute hops using attach_lat_long



"""

from GMeasurements.measurements import RipeAtlasMeasurements
import json

def format_traceroute_result(result:list):

    # clean up probe data
    for probe in result:
        remove_keys = ["fw", "mver", "lts", "endtime", "dst_name", "proto", "af", "size", "paris_id", "timestamp", "msm_name", "from", "type", "group_id", "stored_timestamp"]
        for key in remove_keys:
            probe.pop(key, None)

        # clean up hop data
        # for hop in 

    return result


def retrieve_traceroute_measurement(msm_id):
    measurement = RipeAtlasMeasurements()
    retrieved_measurement = measurement.get_measurement_result(str(msm_id))

    formatted_measurement = format_traceroute_result(result=retrieved_measurement)

    with open(file=f"data/measurement_results/{msm_id}.json", mode='w') as f:
        json.dump(retrieved_measurement, f, indent=4)

    print(retrieved_measurement)

if __name__ == "__main__":
    traceroute_msm_ids = [61984619, 61984618, 61984617, 61984615,61984614]
    retrieve_traceroute_measurement(traceroute_msm_ids[0])