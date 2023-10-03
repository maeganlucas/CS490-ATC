import pandas as pd
from flask import Blueprint, g, make_response
from opensky_api import OpenSkyApi
from requests.exceptions import ReadTimeout

from .map import initial_center

try:
    # try to use the opensky API with credentials
    from ..secrets import OpenSkyCredentials

    opensky = OpenSkyApi(
        username=OpenSkyCredentials.USERNAME, password=OpenSkyCredentials.PASSWORD
    )
except ImportError:
    # if the username/password secrets weren't configured, use without credentials
    opensky = OpenSkyApi()

bp = Blueprint("data", __name__, url_prefix="/data")

airport_data = pd.read_excel(
    "data/us-airports.xlsx",
    usecols=[
        "ident",
        "type",
        "name",
        "latitude",
        "longitude",
        "elevation",
        "country_name",
        "region_name",
        "local_region",
        "municipality",
        "gps_code",
        "iata_code",
        "local_code",
        "home_link",
        "stream_freqs",
    ],
)
#! Table of airport data loaded from the excel sheet in "data/us-airports.xlsx"


@bp.route("/plane_states")
def plane_states():
    """
    Fetches the available plane states from the OpenSky Network API within +/- 3
    degrees of the initial map center (KDAB airport).

    **Endpoint**: ``/data/plane_states``

    :returns: A JSON response with a root node called ``"plane_data"``, which is an array of JSON objects with the following keys:
    * ``icao24`` - (``String`` | ``str``) the ICAO 24-bit address of the plane (hexadecimal)
    * ``callsign`` - (``String`` | ``str``) callsign of the aircraft (e.g. "ER483")
    * ``origin_country`` - (``String`` |``str``) country of origin of the aircraft (e.g. "United States", "Canada", "Peru", etc.)
    * ``time_position`` - (``Number`` | ``int``) Unix time, in milliseconds, of last position update
    * ``last_contact`` - (``Number`` | ``int``) Unix time, in milliseconds, of last contact
    * ``longitude`` - (``Number`` | ``float``) WGS84 longitudinal coordinate of the aircraft
    * ``latitude`` - (``Number`` | ``float``) WGS84 latitudinal coordinate of the aircraft
    * ``geo_altitude`` - (``Number`` | ``float``) geometric altitude of the aircraft (meters)
    * ``on_ground`` - (``Boolean`` | ``bool``) Whether or not the plane is on the ground (true if on the ground, false otherwise)
    * ``velocity`` - (``Number`` | ``float``) Horizontal velocity of the aircraft (meters per second)
    * ``true_track`` - (``Number`` | ``float``) Track/heading of the aircraft. This is a float in the range of [0, 360] (degrees)
    * ``vertical_rate`` - (``Number`` | ``float``) Vertical rate aka rate of ascension (positive vertical rate) or descension (negative vertical rate)
    * ``squawk`` - (``String`` | ``str``) Squawk code of the aircraft, ``null`` if not available
    * ``position_source`` - (``Number`` | ``int``) Source of position information (e.g. ADS-B, FLARM, etc.)
    * ``category`` - (``Number`` | ``int``) Category of the aircraft
    """
    data = {"plane_data": []}

    try:
        states = opensky.get_states(
            bbox=(
                initial_center["lat"] - 3,
                initial_center["lat"] + 3,
                initial_center["lon"] - 3,
                initial_center["lon"] + 3,
            )
        )

        # cache states in case there is a read timeout in the next call
        g.states_cache = states
    except ReadTimeout:
        # reuse cached data if there is a read timeout on the OpenSky API endpoint
        states = g.get("states_cache")

    if states is None:
        return make_response("Too many requests", 500)

    for state in states.states:
        data["plane_data"].append(
            {
                "icao24": state.icao24,
                "callsign": state.callsign,
                "origin_country": state.origin_country,
                "time_position": state.time_position,
                "last_contact": state.last_contact,
                "longitude": state.longitude,
                "latitude": state.latitude,
                "geo_altitude": state.geo_altitude,
                "on_ground": state.on_ground,
                "velocity": state.velocity,
                "true_track": state.true_track,
                "vertical_rate": state.vertical_rate,
                "squawk": state.squawk,
                "position_source": state.position_source,
                "category": state.category,
            }
        )

    return make_response(data, 200)


@bp.route("/flight_track/<icao24>")
def flight_track(icao24):
    """
    Retrieves the flight track information of an aircraft specified by its ICAO 24-bit hexadecimal address.
    Data is retrieved from the OpenSky Network API.

    **Endpoint**: ``/data/flight_track/<icao24>``, ``<icao24>`` should be replaced with the ``icao24`` param (below)

    :param icao24: (required) ``String`` | ``str`` 24-bit hexadecimal address of the aircraft to lookup
    :returns: A JSON response with a root node called ``waypoints``, which is an array of JSON objects with the following keys:
    * ``time`` - (``Number`` | ``int``) Unix time in milliseconds that this waypoint was reached/logged
    * ``latitude`` - (``Number`` | ``float``) WGS84 latitude of the waypoint position
    * ``longitude`` - (``Number`` | ``float``) WGS84 longitude of the waypoint position
    """
    response_data = {"waypoints": []}

    if "flight_tracks" not in g:
        g.flight_tracks = {}

    try:
        track = opensky.get_track_by_aircraft(icao24)
        g.flight_tracks[icao24] = track
    except ReadTimeout:
        track = g.flight_tracks.get(icao24)
    finally:
        flight_path = track.path

    for waypoint in flight_path:
        response_data["waypoints"].append(
            {
                # convert from seconds since unix epoch to milliseconds for compatibility with JS Date API
                "time": waypoint[0] * 1000,
                "latitude": waypoint[1],
                "longitude": waypoint[2],
            }
        )

    return make_response(response_data, 200)


@bp.route("/airports/<state>")
def airports(state):
    """
    Retrieves airport data/metadata by state. This information is modified from the "List of US Airport"
    referenced at the end of the README. Airports are filtered by "large" and "medium" types, since the number
    of airports by state is, frankly, absurd.

    **Endpoint**: ``/data/airports/<state>``, ``<state>`` should be replaced with the ``state`` parameters (below)

    :param state: (required) ``String`` | ``str`` Two letter abbreviation of the state (e.g. FL for Florida)
    :returns: A JSON response with a root node called ``airport_data``, which is an array of JSON objects with the following keys:
    * ``ident`` - (``String`` | ``str``) Airport identification code
    * ``name`` - (``String`` | ``str``) Proper name of the airport
    * ``latitude`` - (``Number`` | ``float``) WGS84 Latitude of the airport
    * ``longitude`` - (``Number`` | ``float``) WGS84 Longitude of the airport
    * ``elevation`` - (``Number`` | ``float``) Elevation of the airport (from sea level), in feet
    * ``region_name`` - (``String`` | ``str``) Name of the region the airport is located within
    * ``local_region`` - (``String`` | ``str``) Local region of the airport
    * ``municipality`` - (``String`` | ``str``) Municipality the airport is located in
    * ``gps_code`` - (``String`` | ``str``) GPS code of the airport
    * ``iata_code`` - (``String`` | ``str``) IATA code of the airport
    * ``local_code`` - (``String`` | ``str``) Local code of the airport
    * ``home_link`` - (``String`` | ``str``) Link to the website/homepage of the airport's website, if available. ``null`` otherwise
    """
    response_data = {"airport_data": []}

    for row in airport_data.itertuples():
        if row.local_region == state:
            # filter by medium and large airports, because I didn't realize just
            # how many airports there are in the US
            if row.type == "large_airport" or row.type == "medium_airport":
                data = {
                    "ident": row.ident,
                    "name": row.name,
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                    "elevation": row.elevation,
                    "region_name": row.region_name,
                    "local_region": row.local_region,
                    "municipality": row.municipality,
                    "gps_code": row.gps_code,
                    "iata_code": row.iata_code,
                    "local_code": row.local_code,
                    "home_link": row.home_link,
                }

                # filter out nan values
                for k, v in data.items():
                    if pd.isna(v):
                        # json lib doesn't encode nan values correctly, but does encode None correctly
                        data[k] = None

                if not pd.isna(row.stream_freqs):
                    data["tower_frequencies"] = row.stream_freqs.split(",")

                response_data["airport_data"].append(data)

    return make_response(response_data)
