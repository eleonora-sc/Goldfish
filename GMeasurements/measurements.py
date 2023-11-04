import datetime
"""


For more information on the ripe atlas rest api 
https://atlas.ripe.net/docs/apis/rest-api-manual/


"""
from typing import Any, Dict, List, Unpack, Required, NotRequired
from requests import request, get, post
import json
from measurement_params import *
from enum import Enum, auto
from dotenv import load_dotenv
from os import getenv
load_dotenv()


class MeasurementType(Enum):
    PING = auto()
    TRACEROUTE = auto()

class ProbeType(Enum):
    AREA = auto()
    COUNTRY = auto()
    PROBES = auto()
    UDM = auto




class Payload():

    def __init__(self):
        self.definitions: List[Dict[str, Any]] = []
        self.probes: List[Dict[str, Any]] = []
        self.payload: Dict[str, Any] = {}

    def _add_definition(self, required_keys, valid_type, all_keys, **kwargs):
        if not required_keys.issubset(kwargs):
            raise ValueError(f"Missing required keys: {required_keys - kwargs.keys()}")

        if kwargs["type"] != valid_type:
            raise ValueError(f"Type must be '{valid_type}'")

        definition = {key: kwargs[key] for key in all_keys if key in kwargs}
        self.definitions.append(definition)

    def add_traceroute_definition(self, **kwargs: Unpack[TracerouteParams]) -> None:
        required_keys = {"target", "description", "type", "af"}
        all_keys = [
            "target", "description", "type", "af", "resolve_on_probe",
            "is_public", "packets", "protocol", "paris", "firsthop",
            "interval", "is_oneoff"
        ]
        self._add_definition(required_keys, "traceroute", all_keys, **kwargs)

    def add_ping_definition(self, **kwargs: Unpack[PingParams]) -> None:
        required_keys = {"target", "description", "type", "af"}
        all_keys = [
            "target", "description", "type", "af", "resolve_on_probe",
            "is_public"
        ]
        self._add_definition(required_keys, "ping", all_keys, **kwargs)

    def add_probe(self, **kwargs:Unpack[PingParams]) -> None:
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
        if len(self.definitions) == 0:
            raise ValueError("No definitions found")
        if len(self.probes) == 0:
            raise ValueError("No probes found")
        return {
            "definitions": self.definitions,
            "probes": self.probes
        }


class RipeAtlasMeasurements():
    def __init__(self, ATLAS_API_KEY):
        self.url = "https://atlas.ripe.net/api/v2/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Key {ATLAS_API_KEY}"
        }
        self.key = ATLAS_API_KEY


    def _post(self, base_url:str, payload:dict, type=None):
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
            return {"error": f"Returned with status code {response.status_code}"}


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


    # def _put(self):
    #     pass

    # def _patch(self):
    #     pass

    # def _delete(self):
    #     pass

    # def get_finished_measurements(self):
    #     pass

    # def get_failed_measurements(self):
    #     pass

    # def get_successful_measurements(self):
    #     pass

    # def get_ongoing_measurements(self):
    #     pass
    
    def get_traceroute_measurement(self, msm_id:str, start:datetime.datetime=None,  stop:datetime.datetime=None):
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
            unix_start = int(start.timestamp()) # requires UNIX timestamp as an integer
            unix_stop = int(stop.timestamp()) # requires UNIX timestamp as an integer
            base_url += f"?start={unix_start}&{unix_stop}"

        response = self._get_json_response(base_url=base_url)
        if type(response) == dict:
            raise ValueError(f"Bad Request in get_probes with error: {response['error']}")

        return response[0] # CAUTION: we are only concerned with one-off traceroute measurements, hence we only grab the first result in the list, which is the only result with one-off traceroute measurements
        
    def get_ping_measurement(self):
        pass

    # def get_measurement_status(self):
    #     pass

    def create_measurement(self, type, payload):
        base_url = "/api/v2/measurements/"

        if type == MeasurementType.TRACEROUTE:
            pass
        elif type == MeasurementType.PING:
            pass

    def create_traceroute_measurement(self, target:str, description:str, af:int, probe_ids:list):
        """
        This function creates a RIPE Atlas traceroute measurement.

        Args:
            target (str): The url or ip of the target of the traceroute measurement.
            description (str): A description of this measurement.
            af (int): either IPv4 (af=4) or IPv6 (af=6)
            probe_ids (list): A list consisting of the IDs (as integers) of the probes participating in this measurement.

        Returns:
            list: List of measurement IDs of the measurements created by this request.
        """

        base_url = "measurements/"
        # construct the payload, some of this should be handled in create_measurements
        payload = {
            "definitions": [
                {
                    "target": target,
                    "description": description,
                    "type": "traceroute",
                    "af": af,
                }
            ],
            "probes": [
                {
                    "type": "probes",
                    "value": ','.join([str(item) for item in probe_ids]), # must be in format: "3045934,230492304,23423423" 
                    "requested": len(probe_ids),
                }
            ],
            "is_oneoff": True,
        }

        measurement_ids = self._post(base_url=base_url, payload=payload) # response is a dict with one field: measurements: [list of measurement ids]
        
        if "error" in measurement_ids.keys():
            raise ValueError(f"Bad Request in get_probes with error: {measurement_ids['error']}")

        return measurement_ids['measurements']


    def create_ping_measurement(self):
        pass

    def create_dns_measurement(self):
        pass

    def stop_measurement(self):
        pass

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
    

