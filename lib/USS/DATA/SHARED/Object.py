__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import sysv_ipc
import struct
import msgpack
import time
from USS.DATA.Object import Object

BLOCK_AVAILABLE=0
BLOCK_NOT_AVAILABLE=1

HEADER_SIG=128
DATA_SIG=255

class Header:
    def stamp(self):
        return self._stamp
    def status(self):
        return self._status
    def key(self):
        return self._key
    def save(self):
        self.object.SharedObject_create_hdr(self.key, self.status)


class SharedObject(Object):
    def __init__(self, key, **argv):
        self.argv = argv
        self.key = key
        self.max_elements = 1
        self.max_element_size = 1024
        self.max_key_length = 128
        try:
            self.sem = sysv_ipc.Semaphore(key)
        except sysv_ipc.ExistentialError:
            self.create()
    def calc_len(self):
        self.hdr1_len   = len(struct.pack("BfBL",HEADER_SIG, 0.0, 0, 0))
        self.hdr_len    = self.hdr1_len*self.max_elements
        self.data1_len  = len(struct.pack("BL",DATA_SIG, 0))+self.max_element_size
        self.data_len   = self.data1_len*self.max_elements
    def create(self):
        self.Object__set_attr("max_elements", self.argv)
        self.Object__set_attr("max_element_size", self.argv)
        self.Object__set_attr("max_key_length", self.argv)
        self.calc_len()
        try:
            self.sem = sysv_ipc.Semaphore(self.key, sysv_ipc.IPC_CREAT)
            print self.sem
            self.data = sysv_ipc.SharedMemory(self.key, size=self.hdr_len+self.data_len, flags=sysv_ipc.IPC_CREAT)
            self.sem.release()
        except KeyboardInterrupt:
            self.sem.release()
            raise AttributeError, "Can't initialize shared instances for key %d"%self.key
        self.__init_buffer()
    def __pack(selfself, data, max_len):
        buf = msgpack.packb(data)
        if len(buf) > max_len:
            raise ValueError, "Data packet larger than permitted"
        return buf
    def __create_hdr(self, key, status=BLOCK_AVAILABLE):
        buf = self.__pack(key, self.max_key_length)
        print "HDR",repr(buf),len(buf)
        return struct.pack("BfBL", HEADER_SIG,time.time(),status,len(buf))+buf
    SharedObject_create_hdr = __create_hdr
    def __create_data(self, data):
        buf = self.__pack(data, self.max_element_size)
        return struct.pack("BL",DATA_SIG,len(buf))+buf
    def __init_buffer(self):
        self.sem.acquire()
        for c in range(self.max_elements):
            shift = c*self.hdr1_len
            hdr = self.__create_hdr("")
            self.data.write(hdr, shift)
            print "MMM",repr(self.data.read(self.hdr1_len+3,shift))
        for c in range(self.max_elements):
            shift = self.hdr_len + (c*self.data1_len)
            data = self.__create_data(None)
            self.data.write(data, shift)
        self.sem.release()
    def header(self, n):
        shift   = n*(self.hdr1_len+self.max_key_length)
        hdr     = self.data.read(self.hdr1_len, shift)
        print "DDD",repr(self.data.read(self.hdr1_len+3,shift))
        _t, _s, _st, _kl = struct.unpack("BfBL", hdr)
        print "AAA",_t, _s, _st, _kl
        print "st",_st,repr(self.data.read(256, 0))
        _hkey = self.data.read(_kl, shift+self.hdr1_len)
        print repr(_hkey)
        if _t != HEADER_SIG:
            raise ValueError, "Header with index %d isn't a header"%n
        h = Header()
        setattr(h, "stamp", _s)
        setattr(h, "status", _st)
        setattr(h, "key", msgpack.unpackb(_hkey))
        setattr(h, "object", self)
        setattr(h, "shift", shift)
        return h
    def __del__(self):
        self.sem.release()
        self.data.remove()
        self.sem.remove()

if __name__ == '__main__':
    s = SharedObject(1)
    h = s.header(0)
    print h.stamp,h.status,h.key
    del h
    del s




