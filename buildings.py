import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']


response = requests.get("https://map-dev.org.ohio-state.edu/map/buildingindex-isolated.php")
html = response.content.decode()


building_numbers = re.findall(r"building=(\d+)", html)

addresses = []

print(f"Loading {len(building_numbers)} Buildings")

for building_number in building_numbers:
  response = requests.get("https://map-dev.org.ohio-state.edu/map/building-isolated.php?building=" + building_number)
  
  html = response.content.decode().replace("\n", "|").replace("\t", "")
  
  match_html = r"<div class=\"column span-9 osu-margin-top\">(.*?)</div>"

  search = re.findall(match_html, html)
  
  match_p = r"<p>(.*?)</p>"
  
  paras = re.findall(match_p, search[0])
  
  address = paras[0].split("|")[-1].strip().replace("<br>", ", ")
  
  addresses.append(address)
  
  print(building_number, address, end="")
  
  input()

print(addresses)
