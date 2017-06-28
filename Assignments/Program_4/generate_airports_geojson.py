'''
This program takes with the same format and name as
https://github.com/rugbyprof/4553-Spatial-DS/raw/master/Resources/Data/WorldData/airports.json
and converts it to a properly formatted geojson file.
It expects the input file to be in the same directory
as it is being run, and outputs to "geo_json/airports_gj.geojson"
'''

import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + "\\airports.json","r")

data = f.read()

data = json.loads(data)

all_airports = {}
all_airports['type'] = 'FeatureCollection'
all_airports['features'] = []

for k,v in data.items():
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
          lon,
          lat
        ]
    all_airports['features'].append(gj)
    
    #we can remove this later
    '''    
    if len(all_airports['features']) == 1000:
        out = open(DIRPATH + "\\geo_json\\1000_airports_gj.geojson","w")
        out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))
        out.close()
    '''

out = open(DIRPATH + "\\geo_json\\airports_gj.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()