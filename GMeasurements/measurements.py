from datetime import datetime
import pandas as pd
"""


For more information on the ripe atlas rest api 
https://atlas.ripe.net/docs/apis/rest-api-manual/


"""
from typing import Any, Dict, List, Unpack, Required, NotRequired
from requests import request, get, post
import json
from GMeasurements.measurement_params import *
from enum import Enum, auto
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Payload():
    def __init__(self):
        self.definitions: List[Dict[str, Any]] = []
        self.probes: List[Dict[str, Any]] = []
        self.payload: Dict[str, Any] = {}
        self.base_measurement_keys ={
            "description", "af", "type", "resolve_on_probe", "is_oneoff", "start_time", "stop_time", "interval", "spread", "is_public"
        }
        self.base_required_keys = {
            "description", "af", "type"
        }
        self.base_start_time = None
        self.base_stop_time = None
        self.base_is_one_off = None

    def _add_definition(self, required_keys, valid_type, all_keys, **kwargs):
        if not required_keys.issubset(kwargs):
            raise ValueError(f"Missing required keys: {required_keys - kwargs.keys()}")

        if kwargs["type"] != valid_type:
            raise ValueError(f"Type must be '{valid_type}'")

        definition = {key: kwargs[key] for key in all_keys if key in kwargs}
        self.definitions.append(definition)

    def add_traceroute_definition(self, **kwargs: Unpack[TracerouteParams]) -> None:
        traceroute_required_keys = {"target"}
        traceroute_all_keys = {
            "target", "response_timeout", "packets", "paris", "size", "first_hop", "max_hops", "protocol"
        }
        required_keys = traceroute_required_keys | self.base_required_keys
        all_keys = traceroute_all_keys | self.base_measurement_keys
        self._add_definition(required_keys, "traceroute", all_keys, **kwargs)

    def add_ping_definition(self, **kwargs: Unpack[PingParams]) -> None:
        ping_required_keys = {"target"}
        ping_all_keys = {
            "target", "packets", "size", "packet_interval", "include_probe_id"
        }
        required_keys = ping_required_keys | self.base_required_keys
        all_keys = ping_all_keys | self.base_measurement_keys
        self._add_definition(required_keys, "ping", all_keys, **kwargs)

    def add_probe(self, **kwargs:Unpack[PingParams]) -> None:
        """
        Adds a probe to the payload.

        Args:
            **kwargs (PingParams): The probe parameters.
            
        """
        probe = {}
        required_keys = {"requested", "type", "value"}
        if not required_keys.issubset(kwargs):
            raise ValueError(f"Missing required keys: {required_keys - kwargs.keys()}")
        types = {"probes", "area", "country", "msm", "prefix", "asn"}
        if kwargs["type"] not in types:
            raise ValueError(f"Type must be one of: {types}")
        probe = {key: kwargs[key] for key in required_keys if key in kwargs}
        self.probes.append(probe)

    def get_payload(self) -> Dict[str, Any]:
        """
        Returns the payload in the format required by the RIPE Atlas API.

        Returns:
            Dict[str, Any]: The payload in the format required by the RIPE Atlas API.
        """
        if len(self.definitions) == 0:
            raise ValueError("No definitions found")
        if len(self.probes) == 0:
            raise ValueError("No probes found")
        return {
            "definitions": self.definitions,
            "probes": self.probes
        }


class RipeAtlasMeasurements():
    def __init__(self, ATLAS_API_KEY=None):
        self.url = "https://atlas.ripe.net/api/v2/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Key {ATLAS_API_KEY}"
        }
        self.key = ATLAS_API_KEY

    def _post(self, base_url:str, payload:dict):
        """
        Performs a post request to the RIPE Atlas v2 API.

        Args:
            base_url (string): _description_
            type (_type_, optional): _description_. Defaults to None.

        Returns:
            list: The response from the API if successful or an error message if unsuccessful.
        """

        request_url = self.url + base_url
        response = post(url=request_url, headers=self.headers, data=json.dumps(payload))

        if(response.status_code == 201):
            return response.json()
        else:
            return {"error": response.json()}

    def _get_json_response(self, base_url, type=None):
        """
        Performs a GET request to the RIPE Atlas v2 API.

        Args:
            base_url (string): The portion of the url that defines what information is retrieved from the API.
            type (_type_, optional): _description_. Defaults to None.

        Returns:
            list/dict: If successful, returns the response from the API, which can be a list or a dict.
            dict: If GET request unsuccessful, returns a dict with the error message.
        """
        request_url = self.url + base_url
        response = get(request_url)
        if(response.status_code == 200):
            return response.json()
        else:
            return {"error": f"Returned with status code {response.status_code}"}
    
    def get_generic_measurement(self, msm_id:str):
        base_url = f"measurements/{msm_id}/"
        response = self._get_json_response(base_url=base_url)
        return response

    def get_measurement_result(self, msm_id:str, start:datetime=None, stop:datetime=None):
        """_summary_

        Args:
            msm_id (str): _description_
            start (datetime.datetime, optional): _description_. Defaults to None.
            stop (datetime.datetime, optional): _description_. Defaults to None.

        Returns:
            dict: The results of the measurement in json format.
        """

        base_url = f"measurements/{msm_id}/results/"

        if start and stop:
            base_url += f"?start_time={start.timestamp()}&stop_time={stop.timestamp()}"
        elif start:
            base_url += f"?start_time={start.timestamp()}"
        elif stop:
            base_url += f"?stop_time={stop.timestamp()}"
        
        response = self._get_json_response(base_url=base_url)
        if type(response) == dict:
            raise ValueError(f"Bad Request in get_probes with error: {response['error']}")

        return response

    def create_measurement(self, type:str, payload:Payload):
        """
        Create a RIPE Atlas measurement.

        Args:
            type (str): What kind of measurement? ping, traceroute
            payload (Payload): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        base_url = "measurements/"
        measurement= self._post(base_url=base_url, payload=payload.get_payload()) # response is a dict with one field: measurements: [list of measurement ids]
        if "error" in measurement:
            raise ValueError(f"Bad Request in create_measurement with error: {measurement['error']}")
        return measurement["measurements"]

    def get_probes(self, **kwargs:Unpack[GetProbesParams]) -> list:
        """ 
        Returns a list of all probes based on the given parameters.

        Args:
            country_code, id__in, asn, asn_v4, asn_v4__in, asn_v6, asn_v6__in, 
            prefix_v4, prefix_v6, status, status_name, tags, include, 
            optional_fields, format, sort (str, Optional): 
                Filters probes based on the specified string values.

            id__lt, id__lte, id__gte, id__gt (int, Optional): 
                Filters probes based on ID values, e.g., id__lt filters for probes with IDs less than the specified value.

            latitude, latitude__lt, latitude__lte, latitude__gte, latitude__gt (str, Optional): 
                Filters probes based on latitude values. `__lt` and `__lte` filter for probes south of the specified value, 
                while `__gte` and `__gt` filter for probes north of the specified value.

            longitude, longitude__lt, longitude__lte, longitude__gte, longitude__gt (str, Optional): 
                Filters probes based on longitude values. `__lt` and `__lte` filter for probes west of the specified value, 
                while `__gte` and `__gt` filter for probes east of the specified value.

            is_anchor, is_public (bool, Optional): 
                Filters probes based on their anchor or public status.

            radius (str, Optional): 
                Filters probes within the specified radius of the supplied latitude and longitude.
                
            status (int, Optional): 
                Probe status (0-Never Connected, 1-Connected, 2-Disconnected, 3-Abandoned).


        Raises:
            ValueError: Raised if the request to the Ripe Atlas API is unsuccessful.

        Returns:
            List[Dict[str, Any]]: A list of probes matching the given parameters. Each probe is represented as:
                {\n
                    "id": probe_id,\n
                    "ipv4": ipv4_address,\n
                    "country_code": country_code,\n
                    "geometry": {"type": type, "coordinates": [lat, lon]},\n
                    "status": {"id": connected_code, "name": connected_status_name, "since": date}\n
                }
        """
        
        base_url = "probes/"
        query_params=""
        IS_PARAMS = False
        for (key,value) in kwargs.items():
            if not IS_PARAMS:
                query_params += "?"
                IS_PARAMS = True
            
        base_url += query_params
        data = self._get_json_response(base_url)
        if "error" in data.keys():
            raise ValueError(f"Bad Request in get_probes with error: {data['error']}")
        total_probes_returned = data["count"]
        probes_list = []
        for probe in data["results"]:
            probe_data = {}
            probe_data["id"] = probe["id"]
            probe_data["ipv4"] = probe["address_v4"]
            probe_data["country_code"] = probe["country_code"]
            probe_data["geometry"] = probe["geometry"]
            probe_data["status"] = probe["status"]
            probe_data["type"] = probe['type']
            probes_list.append(probe_data)
        return probes_list
    

# create_measurement = RipeAtlasMeasurements("4001f1c2-f49d-4727-85f6-62322b76eaac")


# measurement = create_measurement.get_measurement_result("62390085")
# measurement2 = create_measurement.get_generic_measurement("62390085")


# mdf = pd.DataFrame(measurement)

# print(mdf.head())
# mdf.to_csv("test.csv",mode='w',index=False)