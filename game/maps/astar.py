# -*- coding: utf-8 -*-
#======================================================================
#
# astar.py - path finding
#
#======================================================================

import maps
#
# 
#

ToX = 0
ToZ = 0
OpenList = None
OpenIds = None
CloseIds = None

def get_id(x, z):
    Width = maps.MaxX - maps.MinX + 1
    return Width * (z - maps.MinZ) + x - maps.MinX

def get_pos(_id):
    Width = maps.MaxX - maps.MinX + 1
    return int(_id % Width) + maps.MinX, int(_id // Width) + maps.MinZ

def get_cost(x, z):
        return (ToZ - z) * (ToZ - z) + (ToX - x) * (ToX - x)
    
def add_in_open_list(_id, prev, cost):
    if _id in CloseIds or _id in OpenIds:
            return
        
    open_list = OpenList
    open_list.append((_id, prev, cost))
    i = len(open_list) - 1
    
    OpenIds[_id] = True
    
    while True:
        if i == 0:
            break
        top = (i - 1) // 2
        
        if open_list[i][2] >= open_list[top][2]:
            break;
        
        open_list[i], open_list[top] = open_list[top], open_list[i]
        i = top
        
        
def pop_from_open_list():
    open_list = OpenList
    L = len(open_list)
    if L <= 0:
        return None
    if L == 1:
        return open_list.pop()
        
    out = open_list[0]
    open_list[0] = open_list.pop()
    L -= 1
        
    i = 0
    while True:
        v = open_list[i]
        left = i * 2 + 1
        right = i * 2 + 2
        if left < L and v[2] > open_list[left][2]:
            open_list[i], open_list[left] = open_list[left], open_list[i]
            i = left
        elif right < L and v[2] > open_list[right][2]:
            open_list[i], open_list[right] = open_list[right], open_list[i]
            i = right
        else:
            break
        
    return out

def push_neighbor(s):
    x, z = get_pos(s[0])
    # left
    if maps.is_walkable(x - 1, z):
        add_in_open_list(get_id(x-1, z), s, get_cost(x-1, z))
    
    # right
    if maps.is_walkable(x + 1, z):
        add_in_open_list(get_id(x+1, z), s, get_cost(x+1, z))
        
    # up
    if maps.is_walkable(x, z + 1):
        add_in_open_list(get_id(x, z+1), s, get_cost(x, z+1))
        
    # down
    if maps.is_walkable(x, z - 1):
        add_in_open_list(get_id(x, z-1), s, get_cost(x, z-1))
        
               
def path_find(_from_x, _from_z, _to_x, _to_z):
    if not maps.is_walkable(_from_x, _from_z) or not maps.is_walkable(_to_x, _to_z):
        return None
    
    global ToX, ToZ, OpenList, OpenIds, CloseIds
    ToX = _to_x
    ToZ = _to_z
   
    _from_x, _from_z, _to_x, _to_z = int(_from_x), int(_from_z), int(_to_x), int(_to_z)    
    
    ToID = get_id(_to_x, _to_z)
        
    OpenList = []
    OpenIds = {}
    CloseIds = {}
    
    first = (get_id(_from_x, _from_z), None, get_cost(_from_x, _from_z))    
    OpenList.append(first)
    
    loop = 0
    
    while loop < 10000:
        loop += 1
        s = pop_from_open_list()
        if not s:
            return None
        if s[0] == ToID:
            print "Find Path!", loop
            return build_path(s)
        push_neighbor(s)
        
    return None

def build_path(s):
    path = []
    path.append((ToX, ToZ))
    while s != None:
        path.append(get_pos(s[0]))
        s = s[1]
        
    path.reverse()
    
    return path
    
if __name__ == "__main__":
    maps.load("..\\..\\maps")
    print path_find(-2, 0, -7, 2)
        