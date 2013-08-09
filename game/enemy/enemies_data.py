# -*- coding: utf-8 -*-
#======================================================================
#
# enemies_data.py - xxxx
#
#======================================================================

import data

Data = {
        "e1" : {
                "name" : "骷髅战士",
                "hp" : 1000,
                "walk_velocity" : 50,
                "level" : 1,
                "exp" : 5
        },
        "e2" : {
                "name" : "机械杀手",
                "hp" : 100,
                "walk_velocity" : 100,
                "level" : 1,
                "exp" : 3
        }
}

def get_data(name):
    if not name in Data:
        return None
    
    d = Data[name]
    
    out = data.data()

    for k, v in d.items():
        out[k] = v
        
    return out