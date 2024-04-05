from secret_vars import GOOGLE_API_KEY
import requests
import re

import json

# the following need to be manually added at some point
"""
095 - Baker Hall failed: ZERO_RESULTS
200888 - Browning Amphitheater failed: INVALID_REQUEST
200607 - Chadwick Arboretum failed: INVALID_REQUEST
030 - Denney Hall DE failed: ZERO_RESULTS
337 - Dulles Hall DU failed: ZERO_RESULTS
177 - Eleventh Ave, 235-243 W failed: ZERO_RESULTS
201201 - Fred Beekman Park failed: INVALID_REQUEST
201202 - Jesse Owens West Park failed: INVALID_REQUEST
201203 - Lincoln Tower Park failed: INVALID_REQUEST
245 - Physical Activity and Education Services - PAES PE failed: ZERO_RESULTS
246 - Recreation and Physical Activity Center RP failed: ZERO_RESULTS
200605 - The Oval failed: INVALID_REQUEST
"""


def simplifyWhitespaces(string:str) -> str:
  while '  ' in string:
    string = string.replace('  ', ' ')
  return string

def cleanupPara(string:str) -> str:
  tokens = ['</strong>',"<em>","</em>"]
  for token in tokens:
    while token in string:
      string = string.replace(token, "")
  
  return string

response = requests.get("https://map-dev.org.ohio-state.edu/map/buildingindex-isolated.php")
html = response.content.decode()


building_numbers = re.findall(r"building=(\d+)", html)

building_data = dict()

print(f"Loading {len(building_numbers)} Buildings")

for building_number in building_numbers:
  response = requests.get("https://map-dev.org.ohio-state.edu/map/building-isolated.php?building=" + building_number)
  
  html = response.content.decode().replace("\t", "").replace("\n", "|")
  
  div_pattern = r'<div class="column span-9 osu-margin-top">(.*?)</div>'

  div = simplifyWhitespaces(re.findall(div_pattern, html)[0])

  match_p = r'<p>\| <strong>\|(.*?)</p>'
  para = cleanupPara(re.findall(match_p, div)[0])

  building = list(map(lambda x: x.strip(), re.split(r'<br[/]*>[\|]*', para)))
  
  name, *addr = building

  building_data[name] = dict()

  api_req = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={"%20".join(addr)}&key={GOOGLE_API_KEY}').json()

  if api_req['status'] != 'OK':
    print(f'{building_number} - {name} failed: {api_req["status"]}')
    continue

  data = api_req['results'][0]

  building_data[name]['address'] = data["formatted_address"]
  building_data[name]['latitude'] = data["geometry"]["location"]["lat"]
  building_data[name]['longitude'] = data["geometry"]["location"]["lng"]
  building_data[name]['google_place_id'] = data["place_id"]

jsonified = json.dumps(building_data)
print(jsonified, file=open('buildings.json', 'w+'))