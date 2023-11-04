import datetime
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

        request_url = self.url + base_url # + f"?key={self.key}"
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

    def create_measurement(self):
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
        base_url = "probes/"
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




