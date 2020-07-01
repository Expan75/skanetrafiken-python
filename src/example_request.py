# Imports
import json
import os

from lxml import etree
from requests import get


# module specific imports
from client import BASE_URL

# example get call for stations between Malmö-Lund

q = "?inpPointFr=malm%C3%B6&inpPointTo=lund"

full_url = os.path.join(BASE_URL, q)
response = get(
    "http://www.labs.skanetrafiken.se/v2.2/querypage.asp?inpPointFr=malm%C3%B6&inpPointTo=lund"
)
print("Response status: ", response.status_code)


# load input
