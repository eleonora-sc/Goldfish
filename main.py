from logger import Logger
from measurements.create_measurements import CreateMeasurements
from dotenv import load_dotenv
from os import getenv



if __name__ == "__main__":
    load_dotenv()
    logger = Logger()
    ATLAS_API_KEY = getenv("ATLAS_API_KEY")
    create_measurements = CreateMeasurements(ATLAS_API_KEY)
    alaska_nodes = {14300: "Juneau", 51310: "Anchorage 2", 51754: "Anchorage 3", 52344: "Eagle River", 60259: "Anchorage 4", 61113: "Palmer", 61868: "Anchorage 1"}
    # list of targets for traceroute measurements in key value pairs
    traceroute_targets = {62796: "Lagos", 1004023: "Rio", 1005456: "New Delhi", 1006001: "Berlin", 1002558: "Sydney"}
    create_measurements.load_sources(alaska_nodes)
    create_measurements.load_targets(traceroute_targets)
    create_measurements.create_traceroute_measurements()
