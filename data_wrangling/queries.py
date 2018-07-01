from typing import List, Dict
from pymongo.collection import Collection
from supplemental import GeoJSON, geojson_area


def get_tag_types(berlin: Collection) -> str:
    tag_types = list(berlin.aggregate([
        {
            '$group': {'_id': '$_id.type',
                       'count': {'$sum': 1}}
        }
    ]))
    return '\n'.join([f"{t['_id']:9}: {t['count']}"
                      for t in tag_types])


def count_elems(berlin: Collection, name: str) -> int:
    return berlin.find({'_id.type': name}).count()


def count_tags(berlin: Collection, tag: str, value: str) -> int:
    return berlin.find({tag: value}).count()


def get_closest_address(berlin: Collection, coordinate: List[float]):
    near = berlin.aggregate([
        {
            '$geoNear': {
                'near': coordinate,
                'distanceField': 'distance_meters',
                'distanceMultiplier': 6371 * 1000,
                'spherical': True,
                'query': {
                    '_id.type': 'node',
                    'tags.addr:street': {'$exists': True},
                    'tags.addr:housenumber': {'$exists': True}
                }
            }
        },
        {'$limit': 1},
        {
            '$project': {
                'distance_meters': '$distance_meters',
                'coordinates': '$loc.coordinates',
                'addr.street': '$tags.addr:street',
                'addr.house_no': '$tags.addr:housenumber',
                '_id': 0
            }
        }
    ])
    return list(near)[0]


def count_street_types_by_regex(berlin: Collection, regex: str) -> int:
    return list(berlin.aggregate([
        {'$match': {'tags.addr:street': {'$regex': regex}}},
        {'$count': 'count'}
    ]))[0]['count']


def count_street_types_by_suffix(berlin: Collection, regex: str) -> int:
    return count_street_types_by_regex(berlin, regex + '$')


def get_streets_in_region(berlin: Collection, region: GeoJSON) -> List[str]:
    results = list(berlin.aggregate([
        {'$match': {
            'loc': {
                '$geoWithin': {
                    '$geometry': region
                }
            },
            '_id.type': 'node'
        }
        },
        {'$match': {'tags.addr:street': {'$exists': True}}},
        {'$group': {'_id': '$tags.addr:street', 'count': {'$sum': 1}}}
    ]))
    return sorted([result['_id'] for result in results])


def get_streets_per_district(berlin: Collection, districts: Dict[str, GeoJSON]) -> Dict[str, List[str]]:
    results = {}
    for district in sorted(districts.keys()):
        print(f'Finding streets in {district} ...')
        streets = get_streets_in_region(berlin, districts[district])
        results[district] = streets
    return results


def get_district_areas(districts: Dict[str, GeoJSON], scale: float=1.0) -> Dict[str, float]:
    results = {}
    for district, region in districts.items():
        streets = geojson_area(region, scale)
        results[district] = streets
    return results


def count_streets_per_area(streets: Dict[str, List[str]], areas: Dict[str, float]) -> Dict[str, float]:
    counts = {}
    for district in streets.keys():
        count = len(streets[district])
        area = areas[district]
        counts[district] = count / area
    return counts


def get_trees_in_region(berlin: Collection, region: GeoJSON) -> List[str]:
    results = list(berlin.aggregate([
        {'$match': {
            'loc': {
                '$geoWithin': {
                    '$geometry': region
                }
            },
            '_id.type': 'node',
            'tags.natural': 'tree',
        }},
        {'$count': 'count'}
    ]))
    return results[0]['count']
