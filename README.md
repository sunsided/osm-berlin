# OpenStreetMaps Data Wrangling

This project deals with wrangling of OpenStreetMap data of Berlin, Germany.
Two regions were used:

* A custom crop of the Berlin city area.
    * Region: `52.3319824..52.6797125 N`, `13.0709838..13.7741088 E` ([OSM](http://www.openstreetmap.org/#map=11/52.5062/13.4222)).
    * `101 MB` compressed, `1.4 GB` decompressed XML.
* A smaller sample of the Mitte district of Berlin.
    * Region: `52.52912..52.53794 N`, `13.39977..13.40550 E` ([OSM](http://www.openstreetmap.org/#map=17/52.53110/13.40201)).
    * `148 KB` compressed, `1.9 MB` decompressed XML.

Both can be downloaded e.g. by querying the XAPI Compatibility Layer
of the Overpass API (see [here](https://wiki.openstreetmap.org/wiki/Overpass_API/XAPI_Compatibility_Layer)):

```bash
wget -O berlin.osm 'http://www.overpass-api.de/api/xapi?*[bbox=13.0709838,52.3319824,13.7741088,52.6797125][@meta][@timeout=3600]'
wget -O berlin-mitte.osm 'http://www.overpass-api.de/api/xapi?*[bbox=13.39977,52.52912,13.40550,52.53794][@meta]'
```

These are of particular interest to me, because Berlin is my hometown and Berlin Mitte
is the district in which I grew up and went to school.

## OSM XML tag survey

By running the tag extraction script `find_tags.py` on the full Berlin city region the
following [OSM XML](http://wiki.openstreetmap.org/wiki/OSM_XML) tag paths (and the number of their occurrences) were determined:

```
         1 osm
    935054 osm.way
         1 osm.note
         1 osm.meta
   6007591 osm.node
   7429706 osm.way.nd
   2738476 osm.way.tag
   3215139 osm.node.tag
     14715 osm.relation
     78089 osm.relation.tag
    325599 osm.relation.member
```

where `osm ` is the root element.
The smaller Berlin Mitte region, in contrast, contains the following counts:

```
         1 osm
       864 osm.way
         1 osm.note
         1 osm.meta
      7580 osm.node
      8788 osm.way.nd
      2854 osm.way.tag
      5518 osm.node.tag
        40 osm.relation
       332 osm.relation.tag
      2539 osm.relation.member
```

A description of the base elements `node`, `way`, `relation` and `tag`
can be found [here](http://wiki.openstreetmap.org/wiki/Elements).
