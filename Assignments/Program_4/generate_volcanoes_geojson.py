'''
This program takes with the same format and name as
https://github.com/rugbyprof/4553-Spatial-DS/raw/master/Resources/Data/WorldData/world_volcanos.json
and converts it to a properly formatted geojson file.
It expects the input file to be in the same directory
as it is being run, and outputs to "geo_json/volcanoes_gj.geojson"
'''

import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

# the following 'volcanos' is not a typo
# the correct spelling 'volcanoes' is 
# used throughout the rest of this file
f = open(DIRPATH + "\\world_volcanos.json","r")

data = f.read()

data = json.loads(data)

all_volcanoes = {}
all_volcanoes['type'] = 'FeatureCollection'
all_volcanoes['features'] = []

for item in data:
    # some volcanoes don't have a location in the source file
    # so we want to discard these from our geojson file
    if not item["Lat"] == '':
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = item
        lat = float(item['Lat'])
        lon = float(item['Lon'])
        del gj['properties']['Lat']
        del gj['properties']['Lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
              lon,
              lat
            ]
        all_volcanoes['features'].append(gj)
        
        # we can remove this later
        '''
        if len(all_volcanoes['features']) == 1000:
            out = open(DIRPATH + "\\geo_json\\1000_volcanoes_gj.geojson","w")
            out.write(json.dumps(all_volcanoes, sort_keys=False,indent=4, separators=(',', ': ')))
            out.close()
        '''

out = open(DIRPATH + "\\geo_json\\volcanoes_gj.geojson","w")

out.write(json.dumps(all_volcanoes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()