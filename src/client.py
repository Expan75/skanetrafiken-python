# Imports
import json
from requests import get

# Consts [TECHNICALLY CHANGEABLE, DON'T]
BASE_URL = "www.labs.skanetrafiken.se/api.asp/v2.2/querypage.asp"


def get_auth():
    """Helper function for getting auth"""
    return


class Client:
    def __init__(self, format, auth_string):
        self.format = "json"

