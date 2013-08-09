# -*- coding: utf-8 -*-
#======================================================================
#
# maps.py - load maps from file
#
#======================================================================

import struct
import util

MinX = 0
MaxX = 0
MinZ = 0
MaxZ = 0
maps = None

def load(fname):
    with open(fname, "rb") as f:
        head = f.read(4 * 5)
        out = struct.unpack("iiiii", head)
        
        count = out[0]
        
        global MinX, MaxX, MinZ, MaxZ, maps
        MinX = out[1]
        MaxX = out[2]
        MinZ = out[3]
        MaxZ = out[4]
        
        content = f.read(4 * count * 2)
        fmt = "i" * count * 2;
        
        out = struct.unpack(fmt, content)
        
        maps = []
        xsize = MaxX - MinX + 1
        zsize = MaxZ - MinZ + 1
        
        maps = [ [k-k for k in xrange(zsize)] for i in xrange(xsize) ]
        
        for i in xrange(count):
            x = out[i * 2]
            z = out[i * 2 + 1]
            
            xpos = x - MinX
            zpos = z - MinZ
            
            maps[xpos][zpos] = 1            
    fix()
            
            
def is_walkable(x, z):
    if x < MinX or x > MaxX or z < MinZ or z > MaxZ:
        return False
    x = int(x)
    z = int(z)
    xpos = x - MinX
    zpos = z - MinZ
    return maps[xpos][zpos] == 1
    
def find_nearest_walkable(x, z):
    loop = 1000
    curr_step = 0
    steps = 1
    direction = 0
    
    while loop > 0:
        loop -= 1
        if is_walkable(x, z):
            return x, z
        
        if direction == 0:    # right
            x += 1
        elif direction == 1:  # up
            z += 1
        elif direction == 2:  # left
            x -= 1
        else:           # down
            z -= 1
            
        curr_step += 1
        if curr_step >= steps:
            curr_step = 0
            if direction == 1 or direction == 3:
                steps += 1
            direction = (direction + 1) % 4
            
    return x, z

def can_direct_reach(from_x, from_z, to_x, to_z):
    from_x, to_x = from_x - MinX, to_x - MinX
    from_z, to_z = from_z - MinZ, to_z - MinZ
    
    if from_x > to_x:
        from_x, from_z, to_x, to_z = to_x, to_z, from_x, from_z
        
    if to_x > from_x:
        x = int(from_x)
        d = (to_z - from_z) / (to_x - from_x)
        while x <= to_x:
            z = from_z + (x - from_x) * d
            if not is_walkable(x + MinX, z + MinZ):
                return False
            x += 1
                
    if to_z != from_z:
        z = int(from_z)
        sgn = util.sgn(to_z - from_z)
        d = (to_x - from_x) / (to_z - from_z)
        while util.sgn(to_z - z) == sgn:
            x = from_x + (z - from_z) * d
            if not is_walkable(x + MinX, z + MinZ):
                return False
            z += sgn
            
    return True
     
    
    
            
            
# ==================== private =================
def output():
    global maps
    for i, zlist in enumerate(maps):
        for k, v in enumerate(zlist):
            if v == 1:
                print i + MinX, ":", k + MinZ
                
def fix():
    def ifix(x, z):
        global maps
        maps[x - MinX][z - MinZ] = 1
    
    ifix(-7, 6)
    ifix(-6, 6)
    ifix(-7, 7)
    ifix(-6, 7)
    
    ifix(-17, 6)
    ifix(-16, 6)
    ifix(-17, 7)
    ifix(-16, 7)
    
    ifix(-9, 36)
    ifix(-8, 36)
    ifix(-9, 37)
    ifix(-8, 37)
    
    ifix(-24, 17)
    ifix(-24, 16)
    ifix(-24, 15)
    
    for i in xrange(16):
        ifix(-24 + (i % 4), 45 + (i // 4))
    
    for i in xrange(6):
        ifix(-25 + i, 6)
        ifix(-25 + i, 7)
                
        ifix(-17 + i, 44)
            
        
if __name__ == "__main__":
    load("..\\..\\maps")
    output()
            