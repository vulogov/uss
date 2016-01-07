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
DATA_SIG=256


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
        self.hdr1_len   = len(struct.pack("BfB",HEADER_SIG, 0.0, 0))
        self.hdr_len    = self.hdr1_len*self.max_elements
        self.data1_len  = len(struct.pack("BL",DATA_SIG, 0))+self.max_element_size
        self.data_len   = self.data1_len*self.max_elements
    def create(self):
        super(self).__set_attr("max_elements", self.argv)
        super(self).__set_attr("max_element_size", self.argv)
        super(self).__set_attr("max_key_length", self.argv)
        self.calc_len()
        try:
            self.sem = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREAT)
            self.data = sysv_ipc.SharedMemory(key, size=self.hdr_len+self.data_len, flags=sysv_ipc.IPC_CREAT)
            self.sem.release()
        except:
            self.sem.release()
            raise AttributeError, "Can't initialize shared instances for key %d"%self.key
    def __pack(selfself, data, max_len):
        buf = msgpack.packb(data)
        if len(buf) > max_len:
            raise ValueError, "Data packet larger than permitted"
        return buf
    def __create_hdr(self, key):
        return struct.pack("BfB", HEADER_SIG,time.time(),BLOCK_AVAILABLE)+self.__pack(key, self.max_key_length)
    def __create_data(self, data):
        buf = self.__pack(data)
        return struct.pack("BL",DATA_SIG,len(buf))+buf
    def __init_buffer(self):
        self.sem.acquire()
        for c in range(self.max_elements):
            shift = c*self.hdr1_len
            hdr = self.__create_hdr(None)
            self.data.write(hdr, shift)
        for c in range(self.max_elements):
            shift = self.hdr_len + (c*self.data1_len)
            data = self.__create_data(None)
            self.data.write(data, shift)
        self.sem.release()
    def __del__(self):
        self.sem.release()
        self.data.remove()
        self.sem.remove()

if __name__ == '__main__':
    s = SharedObject(1)
    print repr(s.data.read())
    del s




