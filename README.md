# OpenStreetMaps Data Wrangling

This project deals with wrangling of OpenStreetMap data of Berlin, Germany.
Two regions were used:

* A custom crop of the Berlin city area from [Mapzen Metro Extracts](https://mapzen.com/data/metro-extracts/metro/berlin_germany/101748799/Berlin/).
    * Region: `52.3319824..52.6797125 N`, `13.0709838..13.7741088 E` ([OSM](http://www.openstreetmap.org/#map=11/52.5062/13.4222)).
    * `96 MB` compressed, `1.4 GB` decompressed XML.
* A smaller sample of the Mitte district of Berlin.
    * Region: `52.53391..52.52828 N`, `13.19381..13.41020 E` ([OSM](http://www.openstreetmap.org/#map=17/52.53110/13.40201)).
    * `250 KB` compressed, `3.7 MB` decompressed XML.

These are of particular interest to me, because Berlin is my hometown and Berlin Mitte
is the district in which I grew up and went to school.

The directly available Berlin city region from Mapzen was only used to obtain
an overview over the possible tags occurring. It was not used further because it
spans large areas surrounding Berlin (crossing country boundaries as well).
It can be found here:

* Berlin city area from [Mapzen Metro Extracts](https://mapzen.com/data/metro-extracts/metro/berlin_germany/101748799/Berlin/).
    * Region: `51.849..52.994 N`, `12.26..14.699 E` ([OSM](http://www.openstreetmap.org/#map=9/52.4259/13.4789)).
    * `198 MB` compressed, `2.7 GB` decompressed XML.

## OSM XML tag survey

By running the tag extraction script `find_tags.py` on the full Berlin city region the
following [OSM XML](http://wiki.openstreetmap.org/wiki/OSM_XML) tag paths (and the number of their occurrences) were determined:

```
         1 osm
   1733505 osm.way
  11214185 osm.node
         1 osm.bounds
  14418967 osm.way.nd
   4616769 osm.way.tag
   3717622 osm.node.tag
     27798 osm.relation
    131360 osm.relation.tag
    375936 osm.relation.member
```

where `osm ` is the root element.
The smaller Berlin Mitte region, in contrast, contains the following counts:

```
         1 osm
      1527 osm.way
     13089 osm.node
         1 osm.bounds
     16340 osm.way.nd
      4122 osm.way.tag
     10293 osm.node.tag
        90 osm.relation
       656 osm.relation.tag
      4507 osm.relation.member
```

A description of the base elements `node`, `way`, `relation` and `tag`
can be found [here](http://wiki.openstreetmap.org/wiki/Elements).
