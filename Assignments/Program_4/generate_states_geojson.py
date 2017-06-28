'''
This program takes with the same format and name as
https://github.com/rugbyprof/4553-Spatial-DS/raw/master/Resources/Data/WorldData/state_borders.json
and converts it to a properly formatted geojson file.
It expects the input file to be in the same directory
as it is being run, and outputs to "geo_json/states_gj.geojson"
As the input file contains polygons not using the "right hand rule"
required by the most recent geojson standard, and
difficulty was had converting that portion of the data,
the output file is not fully compliant and some
software may produce errors when trying to parse
and display the output file.
'''

from pprint import pprint
import os,sys
import json
import collections
from copy import deepcopy

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + "\\state_borders.json","r")

data = f.read()

data = json.loads(data)

all_states = {}
all_states['type'] = 'FeatureCollection'
all_states['features'] = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''


for item in data:
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = item
    gj["geometry"] = {}
    gj["geometry"]["type"]="MultiPolygon"
    gj["geometry"]["coordinates"] = [gj['properties']['borders']]
    del gj['properties']['borders']
    all_states['features'].append(gj)

out = open(DIRPATH + "\\geo_json\\states_gj.geojson","w")

out.write(json.dumps(all_states, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()