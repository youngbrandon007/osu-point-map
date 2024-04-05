import os
from dotenv import load_dotenv
import requests
import re

def simplifyWhitespaces(string:str) -> str:
  while '  ' in string:
    string = string.replace('  ', ' ')
  return string

load_dotenv()

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']


response = requests.get("https://map-dev.org.ohio-state.edu/map/buildingindex-isolated.php")
html = response.content.decode()


building_numbers = re.findall(r"building=(\d+)", html)

addresses = []

print(f"Loading {len(building_numbers)} Buildings")

for building_number in building_numbers[:10]:
  response = requests.get("https://map-dev.org.ohio-state.edu/map/building-isolated.php?building=" + building_number)
  
  html = response.content.decode().replace("\t", "").replace("\n", "|")
  
  div_pattern = r'<div class="column span-9 osu-margin-top">(.*?)</div>'

  div = simplifyWhitespaces(re.findall(div_pattern, html)[0])

  match_p = r'<p>\| <strong>\|(.*?)</p>'
  para = re.findall(match_p, div)[0]
  
  building = list(map(lambda x: x.strip(), re.split(r'[</strong>]*<br>[\|]*', para)))
  
  name, *addr = building

  addresses.append(building)

  print(f'{name}: {", ".join(addr)}')
