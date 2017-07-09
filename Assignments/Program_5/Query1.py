import sys
import os
import pymongo
import json
import pygame
import math
from mongo_helper import MongoHelper
from pprint import pprint

mh = MongoHelper()

def lonlat_to_xy(lon, lat, maxx, maxy):
    x = int((lon + 180.0) / 360.0 * maxx)
    y = int((lat - 90.0) / 180.0 * -maxy)
    return x, y

def point_query(radius, lon, lat):
    point = (lon, lat)
    results = []
    temp = mh.get_features_near_me('airports', point, radius)
    for item in temp:
        results.append(tuple(item['geometry']['coordinates']))
    return results

def get_path(source, dest):
    points = []

    points.append(source)

    while not points[-1] == dest:
        neighbors = point_query(hop, points[-1][0], points[-1][1])
        closest = points[-1]
        for neighbor in neighbors:
            if haversine(neighbor, dest) == 0.0:
                closest = dest
                break
            elif haversine(neighbor, dest) < haversine(closest, dest):
                closest = neighbor
        if closest == points[-1] or closest in points:
            print("Got stuck")

            return points

        points.append(closest)

    return points

# stolen from mongo_helper
def haversine(p0, p1):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = p0
    lon2, lat2 = p1

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 6371 for km
    return c * r

if __name__ == "__main__":
    DIRPATH = os.path.dirname(os.path.realpath(__file__))

    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    bg = pygame.image.load("blankmap-equirectangular.png")

    dummy, source, dest, hop = tuple(sys.argv)

    hop = float(hop)

    source = mh.get_doc_by_keyword('airports','properties.ap_iata',source)
    source = source[0]['geometry']['coordinates']
    dest = mh.get_doc_by_keyword('airports','properties.ap_iata',dest)
    dest = dest[0]['geometry']['coordinates']

    points = get_path(source, dest)

    adjusted = []

    for point in points:
        adjusted.append(lonlat_to_xy(point[0], point[1], width, height))

    screen.blit(bg, (0, 0))

    pygame.draw.lines(screen, (0, 255, 127), False, adjusted)

    if not haversine(points[-1], dest) == 0.0:
        temp = lonlat_to_xy(dest[0], dest[1], width, height)
        pygame.draw.circle(screen, (255, 0, 0), temp, 5)
    
    pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
