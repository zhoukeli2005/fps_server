# -*- coding: utf-8 -*-
#======================================================================
#
# timer.py - xxxx
#
#======================================================================

import datetime

class timer(object):
    
    def __init__(self):
        self.__start_time = datetime.datetime.now()
        
    def current(self):
        now = datetime.datetime.now()
        time_delta = now - self.__start_time
        result = time_delta.days * 24 * 3600 * 1000.0 + time_delta.seconds * 1000.0 + time_delta.microseconds / 1000.0
        return result
    
gtimer = timer()

if __name__ == "__main__":
    t = timer()
    
    loop = 1000000
    while loop > 0:
        loop -= 1
    
    print t.current()