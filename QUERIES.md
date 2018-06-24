# MongoDB Queries

```javascript
db.runCommand(
   {
     geoNear: "osm_berlin",
     near: { type: "Point", coordinates: [
			13.4024623,
			52.5298522
		] },
     spherical: true,
     query: { '_id.type': "node" }
   }
)
```

```javascript
db.osm_berlin.find( { $text: { $search: "vegan" } } )
```