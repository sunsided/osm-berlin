# Tags to validate

The `addr:postcode` and `addr:suburb` tags must match,
`addr:country` must be `DE` and `addr:city` should be close
to `Berlin` (although that depends on the map size).r

```xml
<node id="670070184" lat="52.5353840" lon="13.4010890" version="11" timestamp="2015-12-22T00:58:47Z" changeset="36097351" uid="881429" user="atpl_pilot">
    <tag k="addr:city" v="Berlin"/>
    <tag k="addr:country" v="DE"/>
    <tag k="addr:housenumber" v="6"/>
    <tag k="addr:postcode" v="10119"/>
    <tag k="addr:street" v="Zionskirchstraße"/>
    <tag k="addr:suburb" v="Mitte"/>
    <tag k="amenity" v="restaurant"/>
    <tag k="contact:phone" v="030 4483719"/>
    <tag k="contact:website" v="http://www.oberwasser-berlin.de/"/>
    <tag k="cuisine" v="regional"/>
    <tag k="internet_access" v="no"/>
    <tag k="name" v="Oberwasser"/>
    <tag k="opening_hours" v="Mo-Sa 18:00+"/>
    <tag k="outdoor_seating" v="no"/>
    <tag k="wheelchair" v="no"/>
  </node>
```

The `ref` tag.

```xml
<node id="697316267" lat="52.5299323" lon="13.4032606" version="7" timestamp="2017-07-01T05:56:15Z" changeset="49958581" uid="66391" user="geozeisig">
    <tag k="amenity" v="post_box"/>
    <tag k="collection_times" v="Mo-Fr 13:00,15:30,17:00,18:15,21:15; Sa 14:00; Su 10:45,21:15"/>
    <tag k="last_checked" v="2016-03-04"/>
    <tag k="operator" v="Deutsche Post"/>
    <tag k="postal_code" v="10119"/>
    <tag k="ref" v="Torstr. 105, 10119 Berlin"/>
  </node>
```