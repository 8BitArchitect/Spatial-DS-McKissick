import sys
import os
import json

class geohelper(object)

  def __init__(self, *params):

    DIRPATH = os.path.dirname(os.path.realpath(__file__))

    self.dbs = []
    for param in params:
      f = open(dirpath + '/geojson/' + param + '.geojson')
      dbs.append(json.loads(f))