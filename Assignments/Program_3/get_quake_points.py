import requests
import json
import sys
import os
import glob

"""
This class helps read the NYC crime data.
Usage:
    fh = FileHelper()

    data = fh.get_data([2017]) #pass year in as list, get data for that year
    data = fh.get_data([2015,2016,2017]) #pass years in as list, get data for those years
"""


def condense_file(data):
    condensed_data = []

    for quake in data['features']:
        keep = {}
        keep['lat'] = quake['geometry']['coordinates'][1]
        keep['lon'] = quake['geometry']['coordinates'][0]
        keep['time'] = quake['properties']['time']
        keep['mag'] = quake['properties']['mag']
        condensed_data.append(keep)

    return condensed_data
    

##########################################################################################

def get_earth_quake_data(year,month=[1,12],minmag=None,maxmag=None,query=True):
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude='+str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude='+str(minmag)
    else:
        minmag = '&minmagnitude='+str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'+type+'?format=geojson&starttime='+str(year)+'-'+str(start_month)+'-01&endtime='+str(year)+'-'+str(end_month)+'-01'+minmag+maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r

# main

path = os.path.dirname(os.path.realpath(__file__))
years = [x for x in range(1960,2018)]
months = [x for x in range(0,12)]

#years = [2017]

rc =[]

f = open(path + '/data/quakes_'+str(years[0])+'-'+str(years[-1])+'.json','w')
for y in years:
    print("Year:%s" % (y))
    r = get_earth_quake_data(y,[1,12],7,None,True)
    f2 = open(path + '/data/quake-'+str(y)+'.json','w')
    f2.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
    f2.close()
    rc += condense_file(r)
f.write(json.dumps(rc, sort_keys=True,indent=4, separators=(',', ': ')))
f.close()

