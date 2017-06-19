import pygame
import random
#from dbscan import *
import sys,os
import pprint as pp
import read_crime_data as rc


# def calculate_mbrs(points, epsilon, min_pts):
#     """
#     Find clusters using DBscan and then create a list of bounding rectangles
#     to return.
#     """
#     mbrs = []
#     #clusters =  dbscan(points, epsilon, min_pts)

#     """
#     Traditional dictionary iteration to populate mbr list
#     Does same as below
#     """
#     # for id,cpoints in clusters.items():
#     #     xs = []
#     #     ys = []
#     #     for p in cpoints:
#     #         xs.append(p[0])
#     #         ys.append(p[1])
#     #     max_x = max(xs) 
#     #     max_y = max(ys)
#     #     min_x = min(xs)
#     #     min_y = min(ys)
#     #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
#     # return mbrs

#     """
#     Using list index value to iterate over the clusters dictionary
#     Does same as above
#     """
#     for id in range(len(clusters)-1):
#         xs = []
#         ys = []
#         for p in clusters[id]:
#             xs.append(p[0])
#             ys.append(p[1])
#         max_x = max(xs) 
#         max_y = max(ys)
#         min_x = min(xs)
#         min_y = min(ys)
#         mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
#     return mbrs


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

def normalize_points(points, width, height, minx=0, miny=0, maxx=0, maxy=0):
  if minx == 0:
    minx = maxx = points[0][0]
    miny = maxy = points[0][1]
    for point in points:
      minx = min(minx, point[0])
      maxx = max(maxx, point[0])
      miny = min(miny, point[1])
      maxy = max(maxy, point[1])

  temp = []
  delta = max(maxx - minx, maxy - miny)
  for point in points:
    normx = int((point[0]-minx)/delta*width)
    normy = int(height-((point[1]-miny)/delta*height))
    temp.append((normx, normy))
  return temp

# Main

DIRPATH = os.path.dirname(os.path.realpath(__file__))

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1000, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('New York Crime')
screen.fill(background_colour)

pygame.display.flip()

colors = {'bronx':(2,120,120),'brooklyn':(128,22,56),'manhattan':(194,35,38),'queens':(243,115,56),'staten_island':(253,182,50)}
boroughs = {}
for borough in colors:
#for borough in ['bronx','brooklyn','manhattan','queens','staten_island']:
  boroughs[borough] = normalize_points(rc.getCrimesList(borough),width,height,913357,121250,1067226,271820)
  #print(boroughs[borough])

# mbrs = calculate_mbrs(points, epsilon, min_pts)

running = True
while running:
  for b in boroughs:
    for p in boroughs[b]:
        #pygame.draw.circle(screen, colors[b], p, 2, 0)
        screen.set_at((p),colors[b])
        #print(p)
    # for mbr in mbrs:
    #     pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.image.save(screen, DIRPATH + '\\crime_map.png')
          running = False
  pygame.display.flip()