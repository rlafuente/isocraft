from nbt import nbt
import sys

nbtfile = nbt.NBTFile(sys.argv[1],'rb')

height = nbtfile['Height'].value
length = nbtfile['Length'].value
width = nbtfile['Width'].value

blocks = nbtfile['Blocks']

for x in range(width):
    for z in range(length):
        for y in range(height):    
            blocktype = blocks.pop()
            print '(%d,%d,%d): %d' % (x, y, z, blocktype)


