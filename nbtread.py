from nbt import nbt
nbtfile = nbt.NBTFile("Terrinha.schematic",'rb')
print nbtfile

height = nbtfile['Height'].value
length = nbtfile['Length'].value
width = nbtfile['Width'].value

blocks = nbtfile['Blocks']

for x in range(width):
    for y in range(height):
        for z in range(length):
            blocktype = blocks.pop()
            print '(%d,%d,%d): %d' % (x, y, z, blocktype)


