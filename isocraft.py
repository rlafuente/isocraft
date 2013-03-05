#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import shoebot

from blockdefs import BLOCKDEFS


# change these!

INPUT_FILE = sys.argv[1]
bot = shoebot.sbot.init_bot(outputfile="output.svg") 

BLOCK_SIZE = 2
ORIGIN_X = 150
ORIGIN_Z = 100
BRIGHTNESS_STEP = 0.05
padding = 1

bot.colormode(bot.RGB)
bot.colorrange(255)

bs = BLOCK_SIZE

def draw_block(x,y, blocktype):
    '''
    draw an isometric square prism; x,y are the coordinates of
    the BOTTOM-CENTER corner, z is the height
    '''
    
    if blocktype in BLOCKDEFS:
        blockcolor = bot.color(*BLOCKDEFS[blocktype])
    else:
        blockcolor = bot.color(64, 64, 64)
    
    # FIXME: z and y should be switched around
    z = bs * 2    

    # no strokes in the inside
    bot.nostroke()

    # LEFT FACE
    # first, set the color
    c = bot.color(blockcolor)
    c.brightness -= BRIGHTNESS_STEP
    bot.fill(c)
    # and draw the path
    bot.beginpath(x, y)
    bot.lineto(x-bs*2, y-bs)
    bot.lineto(x-bs*2, y-bs-z)
    bot.lineto(x, y-z)
    bot.endpath()

    # RIGHT FACE
    # darker
    c = bot.color(blockcolor)
    c.brightness -= BRIGHTNESS_STEP * 2
    bot.fill(c)
    bot.beginpath(x, y)
    bot.lineto(x+bs*2, y-bs)
    bot.lineto(x+bs*2, y-bs-z)
    bot.lineto(x, y-z)
    bot.endpath()

    # TOP FACE
    c = bot.color(blockcolor)
    bot.fill(c)
    bot.beginpath(x, y-z)
    bot.lineto(x+bs*2, y-bs-z)
    bot.lineto(x, y-bs*2-z)
    bot.lineto(x-bs*2, y-bs-z)
    bot.endpath()

def parse_line(line):
    coordtuple, blocktype = line.split(':')
    x, y, z = coordtuple.strip('()').split(',')
    x = int(x)
    y = int(y)
    z = int(z)
    blocktype = int(blocktype.strip())
    return x, y, z, blocktype


if __name__ == '__main__':
    # white background
    bot.background(255, 255, 255)

    # start from 40, 40
    # FIXME: following line exposes a Shoebot bug
    # bot.translate(40, 40)
    # and draw the blocks
    lines = list(open(INPUT_FILE, 'r').readlines())
    # last line holds the coordinates
    max_x, max_y, max_z, bt = parse_line(lines[-1])
    
    # set bot size
    w = max_z*bs*2 + max_x*bs*2 + padding*4*bs
    # FIXME: reliably get proper height
    h = max_z*bs + max_x*bs + 120
    bot.size(w,h) 
    
    origin_x = padding*2*bs + max_z*bs*2
    origin_y = 120
    matrix = np.empty((max_x+1, max_y+1, max_z+1))
    
    TYPES = []
    for line in lines:
        x,y,z,blocktype = parse_line(line)
        matrix[x,y,z] = blocktype
        TYPES.append(blocktype)
    print set(TYPES)
    del lines
        
    # we do a separate loop so we can draw them in order
    for y in range(max_y):
        for x in range(max_x):
            for z in range(max_z):
                blocktype = matrix[x,y,z]
                if blocktype:
                    px = origin_x + (x-z) * (2*bs)
                    pz = origin_y + (x+z) * bs - y*bs*2
                    draw_block(px, pz, blocktype)    
    
    bot.finish()
                    
