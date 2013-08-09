# -*- coding: utf-8 -*-
#======================================================================
#
# network.py - xxxx
#
#======================================================================

import asyncore
import socket
import packet

_callback = None

def init(cb):
    global _callback
    _callback = cb

def loop(s):
    asyncore.loop(s, True, None, 1)

class net_callback(object):
    def do_conn_comes(self, conn):
        raise Exception("must implement")
    
    def do_conn_close(self, conn):
        raise Exception("must implement")
    
    def do_packet(self, conn, pkt):
        raise Exception("must implement")

class listener(asyncore.dispatcher):
    
    def __init__(self, port):
        asyncore.dispatcher.__init__(self);
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        
    def handle_accept(self):
        print "accept new connection"
        pair = self.accept()
        if pair is None:
            return
        print "address:", pair[1]
        conn = connection(pair)

        if _callback:
            _callback.do_conn_comes(conn)

class connection(asyncore.dispatcher):
    def __init__(self, pair):
        self.__sock, self.__addr = pair
        asyncore.dispatcher.__init__(self, self.__sock);
        self.__send_list = None
        self.__read_buffer = ""
        
    def send_packet(self, pkt):
        d = (pkt.pack(), self.__send_list)
        self.__send_list = d
                
    def writable(self):
        return self.__send_list is not None
    
    def handle_read(self):
        data = self.recv(8192)
        if len(data) == 0:
            return
        
        self.__read_buffer += data
        
        # parse & callback
        buf = self.__read_buffer
        size, flag = packet.parse_head(buf)
        while size > 0 and size <= len(buf):
            pkt = packet.packet(flag)
            pkt.unpack(buf[:size])
            buf = buf[size:]            
            size, flag = packet.parse_head(buf)
            if _callback:
                _callback.do_packet(self, pkt)
                
        self.__read_buffer = buf        
        
    def handle_write(self):
        d = self.__send_list
        if not d:
            return
        data = d[0]
        size = self.send(data)
        if size >= len(data):
            self.__send_list = d[1]
            return self.handle_write()
        data = data[size:]
        d[0] = data
    
    def handle_close(self):
        self.close()
        if _callback:
            _callback.do_conn_close(self)

