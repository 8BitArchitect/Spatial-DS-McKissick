#!/bin/bash
mongo world_data --eval "db.dropDatabase()"
mongoimport --db world_data --collection airports       --type json --file airports.geojson        --jsonArray
mongoimport --db world_data --collection meteorites     --type json --file meteorites.geojson       --jsonArray
mongoimport --db world_data --collection volcanoes       --type json --file volcanoes.geojson        --jsonArray
mongoimport --db world_data --collection earthquakes    --type json --file earthquakes.geojson     --jsonArray