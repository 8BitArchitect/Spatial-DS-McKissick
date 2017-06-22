import pygame
import sys,os
import json
import datetime
import math

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

def lat_lon_to_equirectangular(lat,lon,width,height):
    y=int((90.0-lat)/180.0*float(height)+.5)
    x=int((lon+180.0)/360.0*float(width)+.5)
    return (x,y)

def color(intensity):
    if intensity < 4:
        return (0,0,255, (intensity-6)*64-1)
    elif intensity < 6:
        return (math.sin((intensity-4)*math.pi/4)*255,255,0)
    elif intensity < 8:
        return (255,math.sin((intensity-6)*math.pi/4)*255,0)
    else:
        return (255,0,math.sin((intensity-8)*math.pi/4)*255)

if __name__=='__main__':

    DIRPATH = os.path.dirname(os.path.realpath(__file__))

    background_colour = (255,255,255)
    orange = (255,127,63)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    bg = pygame.image.load("blankmap-equirectangular.png")
    #screen.fill(background_colour)

    points = [None] * (2018-1960)

    for p in range(len(points)):
       points[p] = []

    pygame.display.flip()
    f = open(DIRPATH + '/data/quakes_1960-2017.json','r')
    quakes = json.loads(f.read())
    for q in quakes:
        year = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=q['time']/1000)).year
        x,y=lat_lon_to_equirectangular(q['lat'],q['lon'],width,height)
        points[year-1960].append((x,y,q['mag']))
    
    year = minyear = 1960
    screen.blit(bg, (0, 0))

    running = True
    while running:

        pygame.display.set_caption('MBRs '+str(year))
        for p in points[year-1960]:
            #pygame.draw.circle(screen, color(p[2]), (p[0],p[1]), int(p[2]-5),0)
            screen.set_at((p[0],p[1]),color(p[2]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.image.save(screen,DIRPATH+'/'+'earthquakes_'+str(minyear)+('-'+str(year) if year != minyear else '')+'.png')
            if event.type == pygame.MOUSEBUTTONDOWN:
                #clean_area(screen,(0,0),width,height,(255,255,255))
                if event.button == 1:
                    if year < 2017:
                        year += 1
                    else:
                        year = 1960
                        screen.blit(bg, (0, 0))
                elif event.button == 3:
                    minyear = (year + 1 if year < 2017 else 1960)
                    screen.blit(bg, (0, 0))
        pygame.display.flip()
        pygame.time.delay(100)
