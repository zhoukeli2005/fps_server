# -*- coding: utf-8 -*-
#======================================================================
#
# server.py - xxxx
#
#======================================================================

class data(object):
    
    def __init__(self, **kw):
        for k, v in kw.items():
            self.__setattr__(k, v)
    
    def __setattr__(self, k, v):
        self.__dict__[k] = v
        
    def __setitem__(self, k, v):
        self.__setattr__(k, v)
        
    def __getitem__(self, k):
        return self.__getattribute__(k)
        
    def __str__(self):
        out = ""
        for k, v in self.__dict__.items():
            if k[:2] != "__":
                out += k.__str__() + ":" + v.__str__() + ";"
        return out
