from enum import Enum

from flask import Blueprint, render_template

bp = Blueprint("map", __name__, url_prefix="/map")

initial_center = {"lon": -81.0580422, "lat": 29.1799089, "zoom": 8}



#! Initial latitude and longitude set to Daytona Beach. Zoom level found through trial and error


class MapSelector(Enum):
    """
    Map type selector.

    Keys correspond to the URI endpoint for the map type.
    """

    GEOGRAPHIC = "geo"
    #! Geographic map endpoint selector

    SECTIONAL = "aero"
    #! Sectional map endpoint selector


@bp.route("/<type>")
def map(type: str):
    """
    Endpoint for the different types of interactive maps. Renders and returns a template based on the map type.

    **Endpoint**: either ``/map/<type>``, ``<type>`` should be replaced with the ``type`` parameter (below)

    :param type: Map type to display. Can be either `"geo"` or `"aero"`.
    """
    map_type = MapSelector(type)
    if map_type == MapSelector.GEOGRAPHIC:
        return render_template(
            "map/geographic_map.html",
            initial_center=initial_center,
        )

    elif map_type == MapSelector.SECTIONAL:
        return render_template(
            "map/sectional_map.html",
            initial_center=initial_center,
        )
