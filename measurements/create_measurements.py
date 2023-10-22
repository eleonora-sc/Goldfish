from ripe.atlas.cousteau import AtlasSource, AtlasCreateRequest, Ping, Traceroute, Probe
from ripe.atlas.sagan import SslResult
import os
from dotenv import load_dotenv
from datetime import datetime
from api.mongo import add_measurements_to_db, client

class CreateMeasurements:
    def __init__(self, ATLAS_API_KEY:str):
        self.ATLAS_API_KEY = ATLAS_API_KEY
        self.targets = None
        self.target_ips = None
        self.sources = None
        self.sources_str = ""
        self.return_data = None
        self.logger = None

    def load_logger(self, logger):
        self.logger = logger
    
    def __load_target_ips(self):
        target_ips = []
        for i, target in enumerate(self.targets):
            probe = Probe(id=target)
            target_ips.append(probe.address_v4)
            if self.logger:
                self.logger.log(f"{probe.country_code} - {probe.address_v4}")
        self.target_ips = target_ips
        print(self.target_ips)

    def load_targets(self, targets:dict[int, str]):
        """
        This sets self.targets to be used in creating measurements and sets the ips associated with them
        Args:
            :targets dictionary of the target probes in the format {probe_id:"City Name"}
            :type dict[int, str]
        """
        self.targets = targets
        self.__load_target_ips()

    def load_sources(self, source:dict[int,str]):
        self.sources = source
        for i,key in enumerate(self.sources):
            if i < len(self.sources)-1:
                self.sources_str  = self.sources_str + str(key)+","
            else:
                self.sources_str = self.sources_str + str(key)
        print(self.sources_str)


    def create_ping_measurements(self):
        pass

    def create_traceroute_measurements(self):
        traceroute_measurements = []
        if(self.target_ips == None or self.sources == None or self.sources_str == "" or self.targets == None):
            raise ValueError("All data not loaded in")
        for i, target in enumerate(self.target_ips):
            print(f"trying target {i}, with target {target}")
            traceroute = Traceroute(
                af=4, # address family ie ipv4 and ipv6
                target = target,
                description = f"Goldfish OFFICIAL traceroute measurement to {target}",
                protocol="ICMP",
            )
            source = AtlasSource(
                type="probes",
                value=self.sources_str, # must be in this format
                requested=1,
                tags={"include":["system-ipv4-works"]},
            )
            atlas_request = AtlasCreateRequest(
                start_time=datetime.utcnow(),
                key=self.ATLAS_API_KEY,
                measurements=[traceroute],
                sources=[source],
                is_oneoff=True
            )

            (is_success, response) = atlas_request.create()
            print(is_success)
            print(response)
            if is_success:
                traceroute_measurements.append({
                    "sources": self.sources_str,
                    "target": target,
                    "description": f"Goldfish OFFICIAL traceroute measurement to {target}",
                    "measurement_id": response.get("measurements"),
                    "type": "traceroute"
                })
        add_measurements_to_db(traceroute_measurements)


