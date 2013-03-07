#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import numpy as np
from nbt import nbt
import shoebot

from blockdefs import BLOCKDEFS, BLOCKS_WITH_DATA

def draw_block(x, y, blocktype, blockdata, bot):
    '''
    draw an isometric square prism; x,y are the coordinates of
    the BOTTOM-CENTER corner, z is the height
    '''
    
    if blocktype in BLOCKDEFS:
        if blocktype in BLOCKS_WITH_DATA:
            blockcolor = bot.color(*BLOCKDEFS[blocktype][blockdata])
        else:
            blockcolor = bot.color(*BLOCKDEFS[blocktype])
    else:
        blockcolor = bot.color(50, 0, 0)
    
    leftcolor = bot.color(blockcolor)
    leftcolor.brightness -= BRIGHTNESS_STEP
    rightcolor = bot.color(blockcolor)
    rightcolor.brightness -= BRIGHTNESS_STEP * 2
    topcolor = bot.color(blockcolor)

    # FIXME: z and y should be switched around
    z = bs * 2

    bot.nostroke()

    # LEFT FACE
    bot.fill(leftcolor)
    bot.beginpath(x, y)
    bot.lineto(x-bs*2, y-bs)
    bot.lineto(x-bs*2, y-bs-z)
    bot.lineto(x, y-z)
    bot.endpath()

    # RIGHT FACE
    bot.fill(rightcolor)
    bot.beginpath(x, y)
    bot.lineto(x+bs*2, y-bs)
    bot.lineto(x+bs*2, y-bs-z)
    bot.lineto(x, y-z)
    bot.endpath()

    # TOP FACE
    bot.fill(topcolor)
    bot.beginpath(x, y-z)
    bot.lineto(x+bs*2, y-bs-z)
    bot.lineto(x, y-bs*2-z)
    bot.lineto(x-bs*2, y-bs-z)
    bot.endpath()

def get_block_from_nbt(x, y, z, blocks):
    # http://www.minecraftforum.net/topic/16084-baezons-redstone-simulator-v22/page__st__40#entry364309
    # this formula saved my day!
    return blocks[x + z*width + y*length*width]

def remove_invisible_blocks(max_x, max_y, max_z, matrix):
    ray_matrix = np.empty((max_x+1, max_y+1, max_z+1))
    for x in width:
        for y in height:
            ray_matrix[x,y,0] = 5 # wood block

    


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="schematic filename")
    parser.add_argument("-o", "--outputfile", help="output filename (possible extensions are .pdf, .png, .svg and .ps)", dest="outputfile", metavar="FILE")
    parser.add_argument("-v", "--verbose", help="print extra information to terminal", action="store_true")
    parser.add_argument("-r", "--rotation", help="set rotation (0, 90, 180 or 270)", dest="rotation", type=int, default=0)
    parser.add_argument("-p", "--padding", help="set margin (1 = half block width)", dest="padding", type=int, default=1)
    parser.add_argument("-b", "--blocksize", help="individual block size in px (default is 5)", dest="blocksize", type=int, default=1)
    parser.add_argument("-d", "--darken", help="amount to darken each block face (default is 0.05)", dest="darken", type=int, default=0.05)
    args, extra = parser.parse_known_args()

    bs = args.blocksize
    padding = args.padding
    BRIGHTNESS_STEP = args.darken
    if not args.outputfile:
        outfile = os.path.splitext(args.inputfile)[0] + '.png'
    else:
        outfile = args.outputfile

    # read schematics file and determine attributes
    nbtfile = nbt.NBTFile(args.inputfile,'rb')
    height = nbtfile['Height'].value
    length = nbtfile['Length'].value
    width = nbtfile['Width'].value
    blocks = nbtfile['Blocks']
    max_x, max_y, max_z = (width, height, length)
    w = max_z*bs*2 + max_x*bs*2 + padding*4*bs
    # FIXME: reliably get proper height from the y value
    h = max_z*bs + max_x*bs + 120
    data = nbtfile['Data']


    # set up Shoebot
    bot = shoebot.sbot.init_bot(outputfile=outfile) 
    bot.colormode(bot.RGB)
    bot.colorrange(255)
    bot.size(w,h) 
    bot.background(255, 255, 255)
    # determine origin point
    origin_x = padding*2*bs + max_z*bs*2
    origin_y = 120

    # create matrix and populate it with the block values
    # also make a list of block types
    TYPES = []
    matrix = np.empty((max_x+1, max_y+1, max_z+1))
    datamatrix = np.empty((max_x+1, max_y+1, max_z+1))
    i = 0
    for x in range(width):
        for y in range(height):    
            for z in range(length):
                blocktype = get_block_from_nbt(x, y, z, blocks)
                blockdata = data[i]
                matrix[x,y,z] = blocktype
                datamatrix[x,y,z] = blockdata
                TYPES.append(blocktype)
                i += 1
    TYPES.sort()
    blocktypes = set(TYPES)
    for t in blocktypes:
        if t and t not in BLOCKDEFS:
            print 'Unsupported block: %d' % t
    
        
    # apply rotation
    # FIXME: This does not work :(
    if args.rotation:
        from rotation import rotation_matrix
        from math import pi
        axis = [0,1,0]
        theta = rotation * pi/2
        matrix = rotation_matrix(axis, theta, matrix)
        max_x, max_y, max_z = max_z, max_x, max_y

    # we do a separate loop so we can draw them in order
    for y in range(max_y):
        for x in range(max_x):
            for z in range(max_z):
                try:
                    blocktype = matrix[x,y,z]
                except IndexError:
                    i += 1
                    continue
                if blocktype:
                    blockdata = datamatrix[x,y,z]
                    px = origin_x + (x-z) * (2*bs)
                    pz = origin_y + (x+z) * bs - y*bs*2
                    draw_block(px, pz, blocktype, blockdata, bot)
                i += 1
    
    bot.finish()
                    
