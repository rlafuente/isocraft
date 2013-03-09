# -*- coding: utf-8 -*-

# TODO: Add variable value blocks (like wool)
#       See http://www.minecraftwiki.net/wiki/Block_id#Data
# TODO: Expand definition to include texture or more than 1 color

'''
Blocks TODO:
Unsupported block: 130
Unsupported block: 145
Unsupported block: 23
Unsupported block: 42
Unsupported block: 54
Unsupported block: 58
Unsupported block: 77
Unsupported block: 116
Unsupported block: 117
Unsupported block: 118
Unsupported block: 124
'''

BLOCKDEFS = {
  1: (143, 143, 143),  # stone
  2: (116, 81, 55),    # dirt with grass      
  3: (116, 81, 55),    # dirt
  4: (165, 165, 165),  # cobblestone
  5: {                 # wood planks
  		0: '#B4905A',    # oak
        1: '#534028',    # spruce
        2: '#D7C185',    # birch
        3: '#725035',    # jungle
      },
  8: (51, 75, 255),    # water  
  9: (51, 75, 255),    # stationary water
  12: (210, 204, 148), # sand
  17: {                # wood
        0: '#6B5635',  # oak
        1: '#2F1E0B',  # spruce
        2: '#EBEAE0',  # birch
        3: '#57491A',  # jungle
      },
  18: {                # leaves
        0: '#C5D1C0',  # oak
        1: '#758E75',  # pine or spruce
        2: '#8B987D',  # birch
        3: '#145D02',  # jungle
      },
  20: (170, 182, 184), # glass
  24: (210, 204, 148), # sandstone (see data)
  25: (140, 86, 69),   # note block
  26: (177, 57, 53),   # bed
  27: (201, 135, 28),  # powered rail
  28: (137, 117, 88),  # detector rail
  31: (99, 150, 85),   # grass
  33: (178, 144, 92),  # piston
  35: {                # wool
       0: (222, 222, 222), # white
       1: (221, 132, 74),  # orange
       2: (182, 80, 190),  # violet
       3: (104, 136, 200), # light blue
       4: (198, 185, 46),  # yellow
       5: (64, 172, 55),   # lime
       6: (208, 134, 153), # pink
       7: (66, 66, 66),    # dark grey
       8: (162, 168, 168), # light grey
       9: (47, 112, 139),  # teal
       10: (122, 58, 178), # purple
       11: (43, 53, 133),  # dark blue
       12: (87, 55, 34),   # brown
       13: (55, 73, 28),   # green
       14: (152, 53, 50),  # red
       15: (28, 25, 25)},  # black
  37: (234, 242, 2),   # dandelion
  38: (247, 4, 15),    # rose
  43: (172, 172, 172), # double slabs (see data)
  44: (165, 165, 165), # slabs (see data)
  47: (172, 139, 89),  # bookshelf
  49: (50, 50, 50),    # obsidian
  50: (255, 143, 0),   # torch
  53: (186, 151, 97),  # oak wood stairs
  56: (120, 189, 225), # diamond ore
  61: (137, 137, 137), # furnace
  64: (150, 120, 61),  # wooden door
  67: (154, 154, 154), # cobblestone stairs
  68: (168, 137, 82),  # wall sign
  69: (142, 112, 67),  # lever
  70: (137, 137, 137), # stone pressure plate
  71: (205, 205, 205), # iron door
  72: (169, 139, 85),  # wooden pressure plate
  76: (237, 94, 19),   # redstone torch (active)
  79: (133, 180, 255), # ice
  82: (119, 169, 255), # clay
  85: (170, 146, 109), # fence
  88: (91, 71, 58),    # soul sand
  89: (211, 166, 101), # glowstone
  96: (178, 144, 92),  # trapdoor
  102: (193, 224, 229),# glass pane
  126: (178, 144, 92), # wooden slab
  131: (162, 132, 82), # tripwire hook
  134: (178, 144, 92), # spruce wood stairs
  139: (165, 165, 165),# cobblestone wall
  140: (125, 73, 58),  # flower pot
  143: (178, 144, 92), # wooden button
  }

BLOCKS_WITH_DATA = [k for k in BLOCKDEFS if type(BLOCKDEFS[k]) == dict]
