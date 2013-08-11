# -*- coding: utf-8 -*-
#======================================================================
#
# enemies_data.py - xxxx
#
#======================================================================

import data

Data = {
        "e1" : {
                "name" : "e1",
                "hp" : 1000,
                "walk_velocity" : 3,
                "level" : 1,
                "exp" : 5
        },
        "e2" : {
                "name" : "e2",
                "hp" : 100,
                "walk_velocity" : 3.1,
                "level" : 1,
                "exp" : 3
        }
}

def get_data(name):
    if not name in Data:
        print "no enemy:", name
        return None
    
    d = Data[name]
    
    out = data.data()

    for k, v in d.items():
        out[k] = v
        
    return out