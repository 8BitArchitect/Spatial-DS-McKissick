'''
This program takes with the same format and name as
https://github.com/rugbyprof/4553-Spatial-DS/raw/master/Resources/Data/WorldData/world_cities_large.json
and converts it to a properly formatted geojson file.
It expects the input file to be in the same directory
as it is being run, and outputs to "geo_json/cities_gj.geojson"
'''

import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + "\\world_cities_large.json","r")

data = f.read()

data = json.loads(data)

all_cities = {}
all_cities['type'] = 'FeatureCollection'
all_cities['features'] = []

for k,v in data.items():
    for item in v:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = item
        lat = float(item['lat'])
        lon = float(item['lon'])
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
              lon,
              lat
            ]
        all_cities['features'].append(gj)
        
        #we can remove this later
        '''
        if len(all_cities['features']) == 1000:
            out = open(DIRPATH + "\\geo_json\\1000_cities_gj.geojson","w")
            out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))
            out.close()
        '''

out = open(DIRPATH + "\\geo_json\\cities_gj.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()