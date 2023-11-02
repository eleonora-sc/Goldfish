"""


For more information on the ripe atlas rest api 
https://atlas.ripe.net/docs/apis/rest-api-manual/


"""

from requests import request,get, post
import json
from enum import Enum, auto
from dotenv import load_dotenv
from os import getenv

class MeasurementType(Enum):
    PING = auto()
    TRACEROUTE = auto()


class MeasurementDefinitions():
    def __init__(self) -> None:
        self.payload = {
            "definitions":None,
            "probes":None,
        }

    def __init__(self, definitions:list, probes:list):
        self.payload = {
            "definitions": definitions,
            "probes":probes
        }

    
class RipeAtlasMeasurements():
    def __init__(self):
        self.url = "https://atlas.ripe.net"
        self.auth_key = getenv("RIPE_ATLAS_KEY","NONE")
        self.headers = {
            "Authorization" : None
        }

    def _post(self):
        pass

    def _get_json_response(self,base_url, type=None):
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

    def create_measurement(self):
        pass

    def create_traceroute_measurement(self):
        pass

    def create_ping_measurement(self):
        pass

    def create_dns_measurement(self):
        pass

    def stop_measurement(self):
        pass

    def get_probes(self, country_code:str=None, id__lt:int=None, id__lte:int=None, id__gte:int=None, id__gt:int=None,
                   id__in:str=None, radius:tuple[float,float,float]=None, status:int=1) -> list:
        """ 
        Returns a list of all probes based on the given parameters.

        Args:
            country_code (str, optional): Probes with the specified country code. Defaults to None.
            id__lt (int, optional): Probes with ID less than the specified value. Defaults to None.
            id__lte (int, optional): Probes with ID less than or equal to the specified value. Defaults to None.
            id__gte (int, optional): Probes with ID greater than or equal to the specified value. Defaults to None.
            id__gt (int, optional): Probes with ID greater than the specified value. Defaults to None.
            id__in (str, optional): Probes with IDs specified in a comma-separated string. Defaults to None.
            radius (tuple[float, float, float], optional): Description of what the radius tuple represents. Defaults to None.
            status (int, optional): Probe status (0-Never Connected, 1-Connected, 2-Disconnected, 3-Abandoned). Defaults to 1.

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
            probe_data["type"] = probe["type"]
            probes_list.append(probe_data)
        return probes_list
    
    def get_probe(self,id=None):
        args=locals()



measure = RipeAtlasMeasurements()
radius=(61.2176,-149.8997,10)
probes = measure.get_probes(radius=radius)
                
                

