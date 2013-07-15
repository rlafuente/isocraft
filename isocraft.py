#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import numpy as np
from nbt import nbt
import shoebot
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from blockdefs import BLOCKDEFS, BLOCKS_WITH_DATA

def draw_block(x, y, blocktype, blockdata, bot):
    '''
    draw an isometric square prism; x,y are the coordinates of
    the BOTTOM-CENTER corner, z is the height
    '''
    
    blocktype = int(blocktype)
    blockdata = int(blockdata)
    if blocktype in BLOCKDEFS:
        if blocktype in BLOCKS_WITH_DATA:
            try:
                blockcolor = bot.color(BLOCKDEFS[blocktype][blockdata])
            except:
                logging.error('Unsupported block found: type %d, data %d' % (blocktype, blockdata))
                blockcolor = bot.color(50, 0, 0)
        else:
            blockcolor = bot.color(BLOCKDEFS[blocktype])
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
    '''Removes all blocks that are invisible to the observer'''
    ray_matrix = np.empty((max_x+1, max_y+1, max_z+1))
    # draw a box covering the whole area
    for x in range(max_x+1):
        for y in range(max_y+1):
            ray_matrix[x,y,0] = 5 # wood block
    for x in range(max_x+1):
        for z in range(max_z+1):
            ray_matrix[x,max_y,z] = 5 
    for y in range(max_y+1):
        for z in range(max_z+1):
            ray_matrix[0,y,z] = 5

    removed_count = 0
    # send a line from the observer's eye
    # once it bumps into a block, remove all the 
    # following blocks from the original matrix
    for index, v in np.ndenumerate(ray_matrix):
        if not v > 0:
            continue
        x,y,z = index
        logging.debug("BlockRemover: Analysing block (%d, %d, %d)" % (x,y,z))
        found = False
        while 1:
            # get next block
            if matrix[x,y,z] and found:
                # invisible block, remove it
                logging.debug("BlockRemover:   Removing invisible block (%d, %d, %d)" % (x,y,z))
                found = True
                matrix[x,y,z] = 0
                removed_count += 1
            elif matrix[x,y,z]:
                # we found a block, next blocks will be removed
                logging.debug("BlockRemover:   Block found (%d, %d, %d), will remove the others" % (x,y,z))
                found = True
            else:
                # no block, go on
                logging.debug("BlockRemover:   No block at (%d, %d, %d), continuing" % (x,y,z))
                pass
            if x == 0 or y == 0 or z == 0:
                break
            x -= 1
            y -= 1
            z -= 1
    logging.info('Removed %d invisible blocks' % removed_count)
    return matrix

def remove_invisible_blocks_lazy(max_x, max_y, max_z, matrix):
    for index, v in np.ndenumerate(matrix):
        if not v:
            continue
        x,y,z = index
        try:
            leftblock = matrix[x+1, y, z]
            rightblock = matrix[x, y, z+1]
            topblock = matrix[x, y+1, z]
        except IndexError:
            continue
        if leftblock and rightblock and topblock:
            # occluded
            matrix[x,y,z] = 0
    return matrix



def rotate_matrix(matrix, angle=0):
    if not angle:
        return matrix
    # rot90 operates on the first 2 axes, so we switch them for Y rotation
    matrix = np.swapaxes(matrix, 1,2)
    matrix = np.rot90(matrix, angle/90)
    matrix = np.swapaxes(matrix, 1,2)
    return matrix

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="schematic filename")
    parser.add_argument("-o", "--outputfile", help="output filename (possible extensions are .pdf, .png, .svg and .ps)", dest="outputfile", metavar="FILE")
    parser.add_argument("-v", "--verbose", help="print extra information to terminal", action="store_true")
    parser.add_argument("-r", "--rotation", help="set rotation (0, 90, 180 or 270)", dest="rotation", type=int, default=0)
    parser.add_argument("-p", "--padding", help="set margin (1 = half block width)", dest="padding", type=int, default=1)
    parser.add_argument("-b", "--blocksize", help="individual block size in px (default is 5)", dest="blocksize", type=int, default=1)
    parser.add_argument("-d", "--darken", help="amount to darken each block face (default is 0.05)", dest="darken", type=float, default=0.05)
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
    h = max_z*bs + max_x*bs + 400
    data = nbtfile['Data']
    logging.info('Matrix has %d blocks' % len(data))

    # set up Shoebot
    bot = shoebot.sbot.init_bot(outputfile=outfile) 
    bot.colormode(bot.RGB)
    bot.colorrange(255)
    bot.size(w,h) 
    bot.background(255, 255, 255)
    # determine origin point
    origin_x = padding*2*bs + max_z*bs*2
    origin_y = 400

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
                blockdata = get_block_from_nbt(x, y, z, data)
                # blockdata = data[i]
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
    matrix = rotate_matrix(matrix, args.rotation)

    ##########
    matrix = remove_invisible_blocks(max_x, max_y, max_z, matrix)
    # print 'Yay!'
    ##########

    bcount = 0
    # we do a separate loop so we can draw them in order
    for y in range(max_y):
        for x in range(max_x):
            for z in range(max_z):
                try:
                    blocktype = matrix[x,y,z]
                    blockdata = datamatrix[x,y,z]
                except IndexError:
                    i += 1
                    continue
                if blocktype:
                    logging.debug("Drawing block at (%d, %d, %d)" % (x, y, z))
                    px = origin_x + (x-z) * (2*bs)
                    pz = origin_y + (x+z) * bs - y*bs*2
                    draw_block(px, pz, blocktype, blockdata, bot)
                    bcount += 1
                i += 1
    logging.info('Drawn %d blocks' % bcount)
    
    bot.finish()
