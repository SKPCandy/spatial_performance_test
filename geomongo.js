function insertGeo(dbName, colName, num) {
  var col = db.getSiblingDB(dbName).getCollection(colName);
  var unit = 0.001;
  var x;
  var y;

  for (i = 0; i < num; i++) {
    for (j = 0; j < num; j++) {
        x = i * unit;
        y = j * unit;
        col.insert({loc: {type: "Point", coordinates: [ x, y ]}});
    }
  }

  print(col.count());
}

db.test.drop()
insertGeo("geodb", "test", 1000)
