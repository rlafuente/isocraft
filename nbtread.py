from nbt import nbt
import sys
from pprint import pprint

nbtfile = nbt.NBTFile(sys.argv[1],'rb')
height = nbtfile['Height'].value
length = nbtfile['Length'].value
width = nbtfile['Width'].value
blocks = nbtfile['Blocks']

def get_block(x, y, z):
    # http://www.minecraftforum.net/topic/16084-baezons-redstone-simulator-v22/page__st__40#entry364309
    # this formula saved my day!
    # i changed it to correspond to YZX order, according to NBT/Anvil filespec
    return blocks[x + z*width + y*length*width]

for x in range(width):
    for y in range(height):    
        for z in range(length):
            blocktype = get_block(x,y,z)
            print '(%d,%d,%d): %d' % (x, y, z, blocktype)


