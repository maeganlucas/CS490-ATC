from opensky_api import OpenSkyApi
from dotenv import load_dotenv
import os

load_dotenv()

api = OpenSkyApi(
    username=os.getenv("OPENSKY_USERNAME"), password=os.getenv("OPENSKY_PASSWORD")
)


def fetch_opensky(lon_min, lon_max, lat_min, lat_max):
    states = api.get_states(bbox=(lon_min, lon_max, lat_min, lat_max))

    return states.states if states else []
