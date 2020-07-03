# Imports
import json
import os
from requests import get
from pprint import pprint
import xmltodict


# module specific imports
from client import BASE_URL

# example get call for stations between Malmö-Lund

q = "?inpPointFr=malm%C3%B6&inpPointTo=lund"

full_url = os.path.join(BASE_URL, q)
r = get(
    "http://www.labs.skanetrafiken.se/v2.2/querypage.asp?inpPointFr=malm%C3%B6&inpPointTo=lund"
)
print("Response status: ", r.status_code)

xml_string = r.text
parsed_xml = xmltodict.parse(xml_string)
parsed_json = json.dumps(parsed_xml)
# flat_json = flatten(parsed_json)

print(parsed_json[0:1000])

# load input
