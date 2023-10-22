import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
measurement = requests.get(
    "https://atlas.ripe.net/api/v2/measurements/62395910/results/?format=json")

probe = requests.get(
    "https://atlas.ripe.net/api/v2/probes/14300/?format=json"
)
probe = probe.json()

probe_ip = probe['prefix_v4'].split("/")[0]


json_result = measurement.json()
ip_list = []
ip_list.append(probe_ip)

for entry in json_result[0]['result']:
    for result in entry['result']:
        if 'from' in result:
            ip_list.append(result['from'])
            break
geo_location = []
for i, ip in enumerate(ip_list):
    try:
        response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + getenv("IPGEOLOCATION") + "&ip=" + ip + "&output=json",timeout=10)
        geo_location.append(response.json())
    except requests.Timeout:
        continue

for data in geo_location:
    print(data)