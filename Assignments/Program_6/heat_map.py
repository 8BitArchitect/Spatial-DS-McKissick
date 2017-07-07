#Benjamin Shelton, Andrew McKissick, Christian Norfleet
#Spatial Data Structures-Program 6-July 7th, 2017
#This program opens a geojson file of acts of terrorism around the world and creates a heat
#map showing the level of severity of terrorist activity in a certain area
#The heat scale goes from: blue-teal-green-yellow-red from least to most activity respectively

import sys
import os
import json
import pygame
import math
from pprint import pprint

DIRPATH = os.path.dirname(os.path.realpath(__file__))

#opens the geojson file
def read_file():
  f = open(DIRPATH + '\globalterrorism.geojson')

  data = json.loads(f.read())

  attacks = []

  for attack in data:
    attacks.append(attack['geometry']['coordinates'])

  return attacks

#fill out a dictionary with all of the points
def fill_grid(maxx, maxy, points):
  # newpoints = [[0 for i in range(maxy)] for j in range(maxx)]
  newpoints = {}
  for point in points:
    newx = int((point[0] + 180) * maxx / 360)
    newy = int((point[1] - 90) * -maxy / 180)
    if not (newx, newy) in newpoints:
      newpoints[(newx, newy)] = 0
    newpoints[(newx, newy)] += 1

  return newpoints

#helper function for get_gradient
def convert_to_rgb(minval, maxval, val, colors):
  EPSILON = sys.float_info.epsilon  # smallest possible difference

  fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
  i = int(fi)
  f = fi - i
  if f < EPSILON:
    return colors[i]
  else:
    (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
    return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

#determines a scale for the colors based on how many acts of terrorism occured
def get_gradient(minval, maxval, steps, colors):
  gradient = []

  delta = float(maxval-minval) / steps

  for i in range(steps+1):
    val = minval + i*delta
    gradient.append(convert_to_rgb(minval, maxval, val, colors))

  return gradient

#gets the min and max points of a list
def get_minmax(points):
  minval = None
  maxval = None
  for value in points.values():
    if minval == None:
      minval = value
      maxval = value
    else:
      minval = min(minval, value)
      maxval = max(maxval, value)

  return minval, maxval

#this was for fun
def fuzz_grid(grid):
  return

if __name__ == '__main__':
  (width, height) = (2048, 1024)

  points = fill_grid(width, height, read_file())

  minval, maxval = get_minmax(points)

  delta = maxval - minval
  
  colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0), (255, 0, 255)]

  gradient = get_gradient(minval, maxval, 256, colors)

  pprint(gradient)

  #display background image
  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption('Global Terrorism')
  bg = pygame.image.load("blankmap-equirectangular-large.png")

  pygame.display.flip()

  screen.blit(bg, (0, 0))

  running = True

  while running:
    for p in points.items():
      #pygame.draw.circle(screen, color(p[2]), (p[0],p[1]), int(p[2]-5),0)
      # screen.set_at((p[0][0],p[0][1]),gradient[int((p[1] - minval) / delta * 256)])
      screen.set_at((p[0][0],p[0][1]),gradient[int(math.log1p(p[1])/math.log1p(maxval) * 256)])
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.image.save(screen,DIRPATH+'/terrorism.png')
    pygame.display.flip()
    pygame.time.delay(100)