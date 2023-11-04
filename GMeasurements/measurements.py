"""


For more information on the ripe atlas rest api 
https://atlas.ripe.net/docs/apis/rest-api-manual/


"""
from typing import Any, Dict, List, Optional, Unpack, Required, Optional, TypedDict, Union, NotRequired,overload
from requests import request, get, post
import json
from .measurement_params import *
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

    def add_traceroute_definition(self, **kwargs:Unpack[TracerouteParams]) -> None:
        pass

    def add_ping_definition(self,**kwargs:Unpack[PingParams]) -> None:
        pass


    def add_probe(self, **kwargs:Unpack[PingParams]) -> None:
        pass

    def get_payload(self) -> Dict[str, Any]:
        return {
            "definitions": self.definitions,
            "probes": self.probes
        }

    
class RipeAtlasMeasurements():
    def __init__(self):
        self.url = "https://atlas.ripe.net"
        self.auth_key = getenv("ATLAS_API_KEY","NONE")
        print(self.auth_key)
        self.headers = {
            "Authorization" : f"Key {self.auth_key}"
        }

    def _post(self, base_url, data):
        post_url = self.url + base_url
        response = post(post_url,headers=self.headers, data=data)
        return response
    
    def _get_json_response(self,base_url):
        request_url = self.url + base_url
        response = get(request_url)
        if(response.status_code == 200):
            return response.json()
        else:
            return {"error": f"Returned with status code {response.status_code}"}


    def _put(self):
        pass

    def _patch(self):
        pass

    def _delete(self):
        pass

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

    def get_measurement_status(self):
        pass

    def create_measurement(self, type, payload):
        base_url = "/api/v2/measurements/"

        if type == MeasurementType.TRACEROUTE:
            pass
        elif type == MeasurementType.PING:
            pass

    def create_traceroute_measurement(self):
        pass

    def create_ping_measurement(self):
        pass

    def create_dns_measurement(self):
        pass

    def stop_measurement(self):
        pass

    def get_probes(self, country_code:Optional[str]=None, id__lt:Optional[int]=None, id__lte:Optional[int]=None, id__gte:Optional[int]=None, id__gt:Optional[int]=None,
                   id__in:Optional[str]=None, radius:Optional[tuple[float,float,float]]=None, status:int=1) -> list:
        """ 
        Returns a list of all probes based on the given parameters.

        Args:
            country_code (str, Optional): Probes with the specified country code. Defaults to None.
            id__lt (int, Optional): Probes with ID less than the specified value. Defaults to None.
            id__lte (int, Optional): Probes with ID less than or equal to the specified value. Defaults to None.
            id__gte (int, Optional): Probes with ID greater than or equal to the specified value. Defaults to None.
            id__gt (int, Optional): Probes with ID greater than the specified value. Defaults to None.
            id__in (str, Optional): Probes with IDs specified in a comma-separated string. Defaults to None.
            radius (tuple[float, float, float], Optional): Description of what the radius tuple represents. Defaults to None.
            status (int, Optional): Probe status (0-Never Connected, 1-Connected, 2-Disconnected, 3-Abandoned). Defaults to 1.

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
        format="json"
        args = locals()
        base_url = "/api/v2/probes/"
        query_params=""
        IS_PARAMS = False
        for (key,value) in args.items():
            if value is not None and key != "self":
                if IS_PARAMS == False:
                    query_params += "?"
                    IS_PARAMS = True
                else:
                    query_params += "&"
                query_params = query_params + key + "=" + str(value) if not key == "radius" else query_params + key + "="+ f"{value[0]},{value[1]}:{value[2]}"
        base_url += query_params
        data:Dict = self._get_json_response(base_url)
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
    
    def get_probe(self,id=None):
        args=locals()


hello = Payload()

