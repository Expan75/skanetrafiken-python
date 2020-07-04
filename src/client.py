# Imports
import json
import os
import requests as req
from datetime import datetime
import xmltodict
from pprint import pprint


class Client:
    """Client wrapper around Skane API calls. Each method corresponds to get calls on endpoints"""

    def __init__(self):
        self.BASE_URL = "http://www.labs.skanetrafiken.se/v2.2/"
        self.preserve_raw_json = False
        self.current_modes_of_transport = {}

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
        url = (
            self.BASE_URL
            + f"querypage.asp?inpPointTo={str(end)}&inpPointFr={str(start)}"
        )
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
        url = self.BASE_URL + f"neareststation.asp?x={x}&y={y}&Radius={radius}"
        xml_string = req.get(url).text
        parsed_xml = xmltodict.parse(xml_string)

        if self.preserve_raw_json:
            return json.dumps(parsed_xml)
        else:
            # avoids the unessecary nesting
            return json.dumps(
                parsed_xml["soap:Envelope"]["soap:Body"]["GetNearestStopAreaResponse"][
                    "GetNearestStopAreaResult"
                ]
            )

    def get_available_trips(
        self,
        point_to,
        point_from,
        transport_mode,
        cmd_action="search",
        last_start=None,
        first_start=None,
        datetime=datetime.now().strftime("%Y-%m-%d-%H:%M"),
        num_of_journeys=10,
    ):
        """Get travel options from getting between A to B (sel points)

        Args:
            point_to ([string]): destination point name|id|type
            point_from ([string]): departure point name|id|type
            # transport_mode ([type]): [Optional] Sum of linetype ids retrieved from trafficmeans method NOT IMPLEMENTED
            cmd_action ([string]): search|next|previous set of journeys
            last_start ([string]): [Optional] yyyy-mm-dd-hh:mm of last journey in previous results (used in conjunction with cmdAction = next)
            first_start ([string ]): [Optional] yyyy-mm-dd-hh:mm of first journey in previous results (used in conjunction with cmdAction = previous)
            datetime ([datetime]): [Optional] time for journey: yyyy-mm-dd-hh:mm, defaults to now
            num_of_journeys ([int]): [Optional] No of journeys in result, defaults to 10
        """

        # Error handling of less common request arguments
        if (not last_start) & (not first_start):
            pass

        return

    def search_for_station(self, search_string):
        return

    def get_departures_and_arrivals(self):
        return

    def get_traffic_modes(self):
        """Utlity endpoint call for getting all available modes of transportation. 
        Primarily used to update buffer. Returns json
        """
        # setup call and return parsed respose
        url = self.BASE_URL + f"trafficmeans.asp"
        xml_string = req.get(url).text
        parsed_xml = xmltodict.parse(xml_string)

        if self.preserve_raw_json:
            return json.dumps(parsed_xml)
        else:
            return json.dumps(
                parsed_xml["soap:Envelope"]["soap:Body"]["GetMeansOfTransportResponse"][
                    "GetMeansOfTransportResult"
                ]["TransportModes"]["TransportMode"]
            )

    def get_journey_path(self, start, end):
        return


skanetrafiken = Client()
# res = skane.get_start_to_end(start="malmö", end="lund")
# res = skanetrafiken.get_nearest_stations(6167930, 1323215, 5000)
print(skanetrafiken.current_modes_of_transport)
skanetrafiken.current_modes_of_transport = skanetrafiken.get_traffic_modes()
print(skanetrafiken.current_modes_of_transport)
