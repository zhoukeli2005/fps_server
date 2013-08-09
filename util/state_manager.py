# -*- coding: utf-8 -*-
#======================================================================
#
# state_manager.py - state machine
#
#======================================================================

import util.timer

#
#    1. _enter_time 
#    
#
class istate(object):
    
    def __init__(self):
        pass
    
    def enter(self, param):
        pass
    
    def re_enter(self, param):
        pass
    
    def leave(self):
        pass
    
    def update(self):
        pass
    
class istate_manager(object):
    def __init__(self):
        self.__states = {}
        self.__curr_state = None
        self.__curr_state_name = ""
        
    def register(self, name, state):
        if name in self.__states:
            raise Exception("Duplicated States!")
        
        state._statem = self
        self.__states[name] = state
        
    def change_to(self, name, param):
        if not name in self.__states:
            raise Exception("No State:" + name)
        
        s = self.__states[name]
        if s == self.__curr_state:
            self.__curr_state.re_enter(param)
            return
        
        if self.__curr_state:
            self.__curr_state.leave()
            
        self.__curr_state = s
        self.__curr_state_name = name
        
        self.__curr_state._enter_time = util.timer.gtimer.current()
        self.__curr_state.enter(param)
        
    def get_curr_state(self):
        return self.__curr_state
    
    def get_curr_state_name(self):
        return self.__curr_state_name
    
    def update(self):
        if self.__curr_state:
            self.__curr_state.update()