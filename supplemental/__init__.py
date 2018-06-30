import os
import json
from typing import Dict, Any


def get_district_geojson() -> Dict[str, Dict[str, Any]]:
    dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(dir, 'berlin_bezirke_osm_mh.geojson')
    with open(file, 'r') as f:
        data = json.load(f)['features']
    return {d['properties']['name']:d['geometry'] for d in data}


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_district_geojson())
