# -*- coding: utf-8 -*-
#======================================================================
#
# packet.py - xxxx
#
#======================================================================

import struct

register_pool = {}

ENDIAN = ">"
HEAD_FORMAT = ENDIAN + "HH"
HEAD_SIZE = struct.calcsize(HEAD_FORMAT)
STR_SIZE_FORMAT = "I"
STR_SIZE_FORMAT_SIZE = struct.calcsize(STR_SIZE_FORMAT)

def parse_head(raw):
    if len(raw) < HEAD_SIZE:
        return 0, 0
    return struct.unpack(HEAD_FORMAT, raw[:HEAD_SIZE])

def register(flag, _format):
    data = []
    for i in range(len(_format)):
        fmt = _format[i]
        idx = fmt.index(":")
        d = (fmt[0:idx], fmt[idx + 1:].strip())
        data.append(d)
    register_pool[flag] = tuple(data)

class packet(object):
        
    def __init__(self, flag, **kwargs):        
        data = register_pool[flag] 
        self.__flag = flag
        self.__format = data;
        for d in data:
            k = d[0]
            if k in kwargs:
                self.__setattr__(k, kwargs[k])
            else:
                self.__setattr__(k, None)
        
        self.flag = self.__flag

        
    def pack(self):
        curr_format = HEAD_FORMAT
        curr_value = [0, self.__flag]
        for i in range(len(self.__format)):
            key, fmt = self.__format[i]
            value = self.__getattribute__(key)
            if fmt != "s":
                curr_format += fmt
                curr_value.append(value)
            else:
                curr_format += STR_SIZE_FORMAT + "%ds" % len(value)
                curr_value.append(len(value))
                curr_value.append(value)
        curr_value[0] = struct.calcsize(curr_format)
        return struct.pack(curr_format, *curr_value)
    
    def unpack(self, raw):
        raw = raw[HEAD_SIZE:]
        curr_format = ENDIAN
        curr_value = []
        for i in range(len(self.__format)):
            key, fmt = self.__format[i]
            if fmt != "s":
                curr_format += fmt
            else:
                if(len(curr_format) > 1):
                    tmp_len = struct.calcsize(curr_format)
                    curr_value.extend(struct.unpack(curr_format, raw[:tmp_len]))
                    raw = raw[tmp_len:]
                    curr_format = ENDIAN
                    
                sz = struct.unpack(ENDIAN + STR_SIZE_FORMAT, raw[:STR_SIZE_FORMAT_SIZE])[0]
                raw = raw[STR_SIZE_FORMAT_SIZE:]
                tmp_fmt = "%ds" % sz
                tmp_len = struct.calcsize(tmp_fmt)
                curr_value.append(struct.unpack(tmp_fmt, raw[:tmp_len])[0])
                raw = raw[tmp_len:]
        if len(curr_format) > 1:
            curr_value.extend(struct.unpack(curr_format, raw))
        for i in range(len(self.__format)):
            key, fmt = self.__format[i]
            self.__setattr__(key, curr_value[i])
            
    def __str__(self):
        out = ""
        for k, v in self.__dict__.items():
            if k[:2] != "__":
                out += k.__str__() + ":" + v.__str__() + ", "
                
        return out
                    

if __name__ == '__main__':
    MSG_LOGIN = 0x001
    register(MSG_LOGIN, ("name:s", "age:H", "money:H", "desc:s"))
    
    pkt = packet(MSG_LOGIN, name = "zhoukeli", age = 20, money = 1000, desc = "hello world")
    
    s = pkt.pack()
    
    pkt2 = packet(MSG_LOGIN)
    pkt2.unpack(s)
    print pkt2.__dict__
    