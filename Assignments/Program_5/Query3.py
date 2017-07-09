import sys
import os
import pymongo
import json
import pygame
import math
from mongo_helper import MongoHelper
from pprint import pprint
from dbscan import dbscan

# stolen from mongo_helper
def make_result_list(res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

def get_points(results):
    points = []

    for item in results:
        points.append(tuple(item['geometry']['coordinates']))

    return points

def get_mbr(points):
    allx = []
    ally = []
    for point in points:
        allx.append(point[0])
        ally.append(point[1])
    return min(allx), min(ally), max(allx), max(ally)

def adjust_mbr(mbr, maxx, maxy):
    return lonlat_to_xy(mbr[0], mbr[1], maxx, maxy), lonlat_to_xy(mbr[2], mbr[3], maxx, maxy)

def lonlat_to_xy(lon, lat, maxx, maxy):
    x = int((lon + 180.0) / 360.0 * maxx)
    y = int((lat - 90.0) / 180.0 * -maxy)
    return x, y

def dict_to_list(dictionary):
    result = []
    for value in dictionary.values():
        result.append(value)

    return result


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
    (width, height) = (1024, 512)

    colors = {'volcanoes':(255,0,0),'earthquakes':(0,0,255),'meteorites':(0,255,0)}

    dummy, feature, min_pts, eps = sys.argv

    min_pts = float(min_pts)
    eps = float(eps)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    bg = pygame.image.load("blankmap-equirectangular.png")

    client = pymongo.MongoClient()

    results = client['world_data'][feature].find()

    points = get_points(make_result_list(results))

    clusters = dbscan(points, eps, min_pts, haversine)

    del clusters[-1]

    clusters = dict_to_list(clusters)

    clusters = sorted(clusters, key=len)[-5:]

    mbrs = []

    for cluster in clusters:
        mbr = get_mbr(cluster)
        mbrs.append(adjust_mbr(mbr, width, height))

    screen.blit(bg, (0, 0))
    for point in points:
        screen.set_at((lonlat_to_xy(point[0], point[1], width, height)),colors[feature])

    for mbr in mbrs:
        pygame.draw.rect(screen, (255, 127, 0), pygame.Rect(mbr[0], (mbr[1][0] - mbr[0][0], mbr[1][1] - mbr[0][1])), 1)

    pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

