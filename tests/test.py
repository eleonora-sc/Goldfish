# from requests import request, get,post
# import json
# import pandas as pd
# from os import getenv
# from dotenv import load_dotenv
# from pandas_helpers import remove_col
from datetime import datetime 

# # load_dotenv()
# # measurement = requests.get(
# #     "https://atlas.ripe.net/api/v2/measurements/62395910/results/?format=json")

# # probe = requests.get(
# #     "https://atlas.ripe.net/api/v2/probes/14300/?format=json"
# # )
# # probe = probe.json()

# # probe_ip = probe['prefix_v4'].split("/")[0]


# # json_result = measurement.json()
# # ip_list = []
# # ip_list.append(probe_ip)

# # for entry in json_result[0]['result']:
# #     for result in entry['result']:
# #         if 'from' in result:
# #             ip_list.append(result['from'])
# #             break
# # geo_location = []
# # for i, ip in enumerate(ip_list):
# #     try:
# #         response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + getenv("IPGEOLOCATION") + "&ip=" + ip + "&output=json",timeout=10)
# #         geo_location.append(response.json())
# #     except requests.Timeout:
# #         continue

# # for data in geo_location:
# #     print(data)

# country_data = None

# with open('./countries.json', 'r') as file:
#     country_data = json.loads(file.read())

# cdf = pd.DataFrame(country_data)




# cdf_columns = list(cdf.columns)
# cdf_columns.remove('commonName')
# cdf_columns.insert(0,'commonName')
# cdf_columns.remove('officialName')
# cdf_columns.insert(1,'officialName')
# cdf = cdf[cdf_columns]
# cdf.to_csv('./countries.csv',mode='w',index=False)
# cdf.to_json('./countries.json',mode='w',index=False,indent=4)

print(int(datetime(2023,11,9,20,41).timestamp()))

target = {"Barrow":"24.237.124.4"}
print(target.items())
