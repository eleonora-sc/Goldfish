"""


For more information on the ripe atlas rest api 
https://atlas.ripe.net/docs/apis/rest-api-manual/


"""

import requests
import json
from dotenv import load_dotenv
from os import getenv

class RipeMeasurement():
    def __init__(self):
        self.base_url = "https://atlas.ripe.net/"
        self.auth_key = getenv("RIPE_ATLAS_KEY","NONE")
        self.post_header = "Authorization: Key " + self.auth_key

    def get_finished_measurements(self):
        pass

    def get_failed_measurements(self):
        pass

    def get_successful_measurements(self):
        pass

    def get_ongoing_measurements(self):
        pass
    
    def get_traceroute_measurement(self,**kwargs):
        pass
        

    def get_ping_measurement(self):
        pass

    def stop_measurement(self):
        pass

    def measurement_status(self):
        pass

    def create_measurement(self):
        pass

    def create_traceroute_measurement(self):
        pass

    def create_ping_measurement(self):
        pass

    def create_dns_measurement(self):
        pass


