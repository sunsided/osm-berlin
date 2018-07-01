import os
import json
from typing import Dict, Any, Optional, Union
from area import area


GeoJSON = Dict[str, Any]


def get_district_geojson(district: Optional[str] = None) -> Union[Dict[str, GeoJSON], GeoJSON]:
    """
    Gets the Berlin districts or a single one of them (if a district name is specified).
    :param district: The optional district to return; if None, all are returned.
    :return: The district or dictionary of districts.
    """
    dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(dir, 'berlin_bezirke_osm_mh.geojson')
    with open(file, 'r') as f:
        data = json.load(f)['features']
    districts = {d['properties']['name']: d['geometry'] for d in data}
    return districts if district is None else districts[district]


def geojson_area(geojson: GeoJSON, scale: float = 1.0) -> float:
    """
    Gets the area of a GeoJSON object.
    :param geojson: The GeoJSON object.
    :param scale: The scale; for km, use 0.001.
    :return: The area.
    """
    a = area(geojson)
    return a * (scale ** 2)


if __name__ == '__main__':
    from pprint import pprint
    districts = get_district_geojson()
    pprint(districts)
    print('Berlin Mitte is', geojson_area(districts['Mitte'], 0.001), 'km².')
