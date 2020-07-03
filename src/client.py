# Imports
import json
import os
import requests as req
import xmltodict


BASE_URL = "http://www.labs.skanetrafiken.se/v2.2/"

# Helper function
def xml_parser(xml_string):
    """ Utility function for parsing xml_strings into json"""
    return json.dumps(xmltodict.parse(xml_string))


class Client:
    """Client wrapper around Skane API calls. Each method corresponds to get calls on endpoints"""

    def __init__(self):
        self.preserve_raw_json = False

    def get_start_to_end(self, start, end):
        """Restlike endpoint method for getting a travelplan between 2 locations/stations/busstops.

        Args:
            start ([str], optional): Starting point, can be a POI or station/stop. Defaults to None.
            end ([str], optional): End point, can be a POI or station/stop. Defaults to None.

        Returns:
            Json string: defaults to returning a json response of points inbetween. 
        """

        if (start == None) | (end == None):
            Exception("Please provide a startpoint and an endpoint")

        # setup url, send request and return formatted response
        url = BASE_URL + f"querypage.asp?inpPointTo={str(end)}&inpPointFr={str(start)}"
        xml_string = req.get(url).text
        parsed_xml = xmltodict.parse(xml_string)

        # Return either raw or a less nested version
        if self.preserve_raw_json:
            return json.dumps(parsed_xml)
        else:
            return json.dumps(
                parsed_xml["soap:Envelope"]["soap:Body"]["GetStartEndPointResponse"][
                    "GetStartEndPointResult"
                ]
            )

    def get_nearest_stations(self, x, y, radius):
        """Gets the nearest stations to a given location within a given radius.

        Args:
            x ([int]): longitude 
            y ([int]): latitude
            radius ([int]): search radius in meters. Range(1,5000).  

        Returns:
            [json]: Defaults to returning a less nested response of nearest travel stops.
        """

        # Error handling
        try:
            assert (type(x) == int) & (
                type(y == int)
            ), "get_nearest_stations requires an iterable /w (long,lat)"
            assert type(radius) == int
            assert (
                1 <= radius <= 5000
            ), "get_nearest_stations accepts a radius from 1 to 5000m"
        except:
            Exception(
                "Please provide valid arguments when calling get_nearest_stations((long, lat), radius=int)"
            )

        # setup call and return parsed respose
        url = BASE_URL + f"neareststation.asp?x={x}&y={y}&Radius={radius}"
        xml_string = req.get(url).text
        parsed_xml = xmltodict.parse(xml_string)

        if self.preserve_raw_json:
            return json.dumps(parsed_xml)
        else:
            return json.dumps(
                parsed_xml["soap:Envelope"]["soap:Body"]["GetNearestStopAreaResponse"][
                    "GetNearestStopAreaResult"
                ]
            )


skanetrafiken = Client()
# res = skane.get_start_to_end(start="malmö", end="lund")
# res = skanetrafiken.get_nearest_stations(6167930, 1323215, 5000)
print(res)
