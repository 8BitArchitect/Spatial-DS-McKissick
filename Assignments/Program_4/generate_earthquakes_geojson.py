'''
This program takes with the same format and name as
https://github.com/rugbyprof/4553-Spatial-DS/raw/master/Resources/Data/WorldData/earthquakes-1960-2017.json
and converts it to a properly formatted geojson file.
It expects the input file to be in the same directory
as it is being run, and outputs to "geo_json/earthquakes_gj.geojson"
'''

import pprint as pp
import os,sys
import json
import collections
from copy import deepcopy

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + "\\earthquakes-1960-2017.json","r")

data = f.read()

data = json.loads(data)

all_earthquakes = {}
all_earthquakes['type'] = 'FeatureCollection'
all_earthquakes['features'] = []

for k,v in data.items():
    for item in v:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = item
        # this could be done in a simpler manner,
        # but we want to enforce proper element
        # order in the resulting geojson dictionary
        gj["geometry"] = {}
        gj["geometry"]['type'] = 'Point'
        del gj['properties']['geometry']['coordinates'][2]
        gj['geometry']['coordinates'] = deepcopy(gj['properties']['geometry']['coordinates'])
        del gj['properties']['geometry']
        all_earthquakes['features'].append(gj)
        
        #we can remove this later
        '''
        if len(all_earthquakes['features']) == 1000:
            out = open(DIRPATH + "\\geo_json\\1000_earthquakes_gj.geojson","w")
            out.write(json.dumps(all_earthquakes, sort_keys=False,indent=4, separators=(',', ': ')))
            out.close()
        '''

out = open(DIRPATH + "\\geo_json\\earthquakes_gj.geojson","w")

out.write(json.dumps(all_earthquakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()