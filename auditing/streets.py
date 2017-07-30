import re


def is_street_name(elem):
    assert 'k' in elem.attrib and 'v' in elem.attrib
    return elem.attrib['k'] == 'addr:street'
