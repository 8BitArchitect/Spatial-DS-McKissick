import sys
import os
import pymongo
import json
import pygame
from mongo_helper import MongoHelper
from pprint import pprint

METERS_PER_MILE = 1609.34

mh = MongoHelper()

def xy_to_lonlat(x, y, maxx, maxy):
    lon = x/maxx * 360.0 - 180.0
    lat = y/maxy * -180.0 + 90.0
    return lon, lat

def lonlat_to_xy(lon, lat, maxx, maxy):
    x = int((lon + 180.0) / 360.0 * maxx)
    y = int((lat - 90.0) / 180.0 * -maxy)
    return x, y

def point_query(radius, lon, lat):
    results = {'volcanoes': [], 'earthquakes': [], 'meteorites': []}
    point = (lon, lat)
    for key in results:
        temp = mh.get_features_near_me(key, point, radius)
        for item in temp:
            results[key].append(tuple(item['geometry']['coordinates']))
    return results

def filtered_query(radius, lon, lat, collection, field, field_value, minmax, max_results):
    results = {'volcanoes': [], 'earthquakes': [], 'meteorites': []}
    point = (lon, lat)
    temp = mh.get_features_near_me(collection, point, radius)
    if minmax.lower() == 'min':
        gen = (x for x in temp if float(x['properties'][field]) > float(field_value))
    elif minmax.lower() == 'max':
        gen = (x for x in temp if float(x['properties'][field]) < float(field_value))
    else:
        gen = (x for x in temp if x['properties'][field] == field_value)
    for item in gen:
        if not item['properties'][field] == None:
            results[collection].append(tuple(item['geometry']['coordinates']))

    if not max_results == 0:
        results[collection] = results[collection][:max_results]

    return results

# main below here

if __name__ == "__main__":
    DIRPATH = os.path.dirname(os.path.realpath(__file__))

    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    bg = pygame.image.load("blankmap-equirectangular.png")

    fields = {'volcanoes': [], 'earthquakes': [], 'meteorites': []}
    fields['volcanoes'] = ['Name','Altitude','Type']
    fields['earthquakes'] = ['rms', 'magType', 'year', 'depth', 'sig', 'mag', 'time', 'types']
    fields['meteorites'] = ['nametype', 'recclass', 'name', 'year', 'mass', 'fall', 'id']

    func = point_query

    lat = lon = dummy = feature = field = field_value = minmax = max_results = radius = coords = None
        
    if len(sys.argv) == 8:
        dummy, feature, field, field_value, minmax, max_results, radius, coords = tuple(sys.argv)
        lon, lat = coords.split(',')
    elif len(sys.argv) == 7:
        dummy, feature, field, field_value, minmax, max_results, radius = tuple(sys.argv)
    elif len(sys.argv) == 2:
        radius = sys.argv[1]
    else:
        print("ERROR: Unexpected number of arguments. Expected 1, 7, or 8 and got " + str(len(sys.argv)))
        sys.exit(1)

    if not feature == None:
        func = filtered_query
        if not feature in fields:
            print("ERROR: Unexpected feature value. Expected volcanoes, earthquakes, or meteorites and got " + feature)
            sys.exit(1)
        elif not field in fields[feature]:
            print("ERROR: Unexpected field value. Expected one of the following: " + str(fields[feature]) + " and got " + field)
            sys.exit(1)
        if not lon == None:
            lon = float(lon)
            lat = float(lat)
        max_results = int(max_results)
    radius = float(radius)

    screen.blit(bg, (0, 0))

    if not lon == None:
        points = func(radius, lon, lat, feature, field, field_value, minmax, max_results)

        for point in points['volcanoes']:
            screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(255, 0, 0))
        for point in points['meteorites']:
            screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(0, 255, 0))
        for point in points['earthquakes']:
            screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(0, 0, 255))

    pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(bg, (0, 0))
                x, y = tuple(event.pos)
                lon, lat = xy_to_lonlat(x, y, width, height)
                
                points = func(radius, lon, lat, feature, field, field_value, minmax, max_results)

                for point in points['volcanoes']:
                    screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(255, 0, 0))
                for point in points['meteorites']:
                    screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(0, 255, 0))
                for point in points['earthquakes']:
                    screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),(0, 0, 255))
                pygame.display.flip()