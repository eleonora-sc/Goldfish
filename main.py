from GMeasurements.measurements import RipeAtlasMeasurements
from dotenv import load_dotenv
from os import getenv
import json
import csv

if __name__ == "__main__":
    load_dotenv()
    auth_key = getenv("ATLAS_API_KEY","NONE")
    if auth_key == "None":
        raise("error getting atlas api key")
    
    # create an instance of class RipeAtlasMeasurement that can be used for a lot of different measurements
    measurement = RipeAtlasMeasurements(ATLAS_API_KEY=auth_key)

    # # TESTING SUCCESSFUL: get_traceroute_measurement
    # # msm1 = measurement.get_traceroute_measurement(61984619)

    # # TESTING SUCCESSFUL: create_traceroute_measurement
    # probe_list = [60259]
    # new_measurement = measurement.create_traceroute_measurement(description="testing", target="ripe.net", af=4, probe_ids=probe_list)

    # TESTING PING MEASUREMENT CREATION
    new_measurement = measurement.create_measurement()

    # appends measurement ids to this csv
    with open("data/measurements/test_measurements.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        for measurement in new_measurement:
            writer.writerow([measurement])

    # CREATE CONTINUOUS PING MEASUREMENTS
    # new_measurement = 
    
    # with open("data/measurements/ping_measurements.csv", mode='a', newline='') as f:
    #     writer = csv.writer(f)
    #     for measurement in new_measurement:
    #         writer.writerow([measurement])
