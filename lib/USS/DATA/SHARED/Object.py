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
    def Key(self, key):
        self._key = key
    def commit(self, lock=True):
        hdr = self.object.SharedObject_create_hdr(self._key, self._status)
        if lock:
            self.object.sem.acquire()
        self.object.data.write(hdr, self.shift)
        if lock:
            self.object.sem.release()
    def available(self):
        self._status = BLOCK_AVAILABLE
    def not_available(self):
        self._status = BLOCK_NOT_AVAILABLE
    def Data(self):
        return self.object.Data(self.n)
    def remove(self):
        self.not_available()
        self.commit()

class Data:
    def value(self):
        return self._data
    def set(self, data, key=None, **argv):
        _lock = True
        if argv.has_key("lock") and argv["lock"]:
            _lock = argv["lock"]
        if _lock:
            self.object.sem.acquire()
        self._data = data
        _d_buf = self.object.SharedObject_create_data(data)
        h = self.object.Header(self.n)
        if key:
            h.Key(key)
        h.not_available()
        h.commit(False)
        self.object.data.write(_d_buf, self.shift)
        if _lock:
            self.object.sem.release()
    def Header(self):
        return self.object.Header(self.n)
    def commit(self):
        self.set(self._data)

class SharedObject(Object):
    def __init__(self, key, **argv):
        self.argv = argv
        self.key = key
        self.max_elements = 1
        self.max_element_size = 1024
        self.max_key_length = 128
        try:
            self.sem = sysv_ipc.Semaphore(key)
            self.calc_len()
            self.data = sysv_ipc.SharedMemory(self.key, size=self.hdr_len+self.data_len, flags=sysv_ipc.IPC_CREAT)
            self.is_new = False
        except sysv_ipc.ExistentialError:
            self.create()
        print self.data.key
    def calc_len(self):
        self.Object__set_attr("max_elements", self.argv)
        self.Object__set_attr("max_element_size", self.argv)
        self.Object__set_attr("max_key_length", self.argv)
        self.hdr1_len   = len(struct.pack("!BfBL",HEADER_SIG, 0.0, 0, 0))
        self.hdr2_len   = self.hdr1_len + self.max_key_length
        self.hdr_len    = self.hdr2_len*self.max_elements
        self.data1_len  = len(struct.pack("!BL",DATA_SIG, 0))
        self.data2_len  = self.data1_len + self.max_element_size
        self.data_len   = self.data2_len*self.max_elements
    def create(self):
        self.is_new = True
        self.calc_len()
        try:
            self.sem = sysv_ipc.Semaphore(self.key, sysv_ipc.IPC_CREAT)
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
        return struct.pack("!BfBL", HEADER_SIG,time.time(),status,len(buf))+buf.ljust(self.max_key_length, '\0')
    SharedObject_create_hdr = __create_hdr
    def __create_data(self, data):
        buf = self.__pack(data, self.max_element_size)
        return struct.pack("!BL",DATA_SIG,len(buf))+buf.ljust(self.max_element_size, '\0')
    SharedObject_create_data = __create_data
    def __init_buffer(self):
        self.sem.acquire()
        for c in range(self.max_elements):
            shift = c*self.hdr2_len
            hdr = self.__create_hdr("")
            self.data.write(hdr, shift)
        for c in range(self.max_elements):
            shift = self.hdr_len + (c*self.data2_len)
            data = self.__create_data(None)
            self.data.write(data, shift)
        self.sem.release()
    def Header(self, n):
        shift   = n*(self.hdr1_len+self.max_key_length)
        hdr     = self.data.read(self.hdr1_len, shift)
        _t, _s, _st, _kl = struct.unpack("!BfBL", hdr)
        _hkey = self.data.read(_kl, shift+self.hdr1_len)
        if _t != HEADER_SIG:
            raise ValueError, "Header with index %d isn't a header (%d)"%(n, _t)
        h = Header()
        setattr(h, "_stamp", _s)
        setattr(h, "_status", _st)
        setattr(h, "_key", msgpack.unpackb(_hkey))
        setattr(h, "object", self)
        setattr(h, "shift", shift)
        setattr(h, "n", n)
        return h
    def Data(self, n):
        shift   = self.hdr_len + (n*self.data2_len)
        _d_buf = self.data.read(self.data1_len, shift)
        _d_sig, _d_len = struct.unpack("!BL",_d_buf)
        if _d_sig != DATA_SIG:
            raise ValueError, "Data with index %d isn't a data block (%d)"%(n, _d_sig)
        _d = self.data.read(_d_len, shift+self.data1_len)
        d = Data()
        setattr(d, "_data", msgpack.unpackb(_d))
        setattr(d, "object", self)
        setattr(d, "shift", shift)
        setattr(d, "n", n)
        return d
    def Status(self):
        out = []
        for c in range(self.max_elements):
            h = self.Header(c)
            out.append(h.status())
        return out
    def Available(self):
        self.sem.acquire()
        status = self.Status()
        try:
            ix = status.index(BLOCK_AVAILABLE)
            d = self.Data(ix)
            h = d.Header()
            h.not_available()
            h.commit(False)
            self.sem.release()
            return d
        except:
            self.sem.release()
            return None
    def close(self):
        self.sem.release()
        self.data.remove()
        self.sem.remove()

if __name__ == '__main__':
    s = SharedObject(1, max_elements=10)
    while True:
        d = s.Available()
        if not d:
            break
        d.set("a", "key")
    print s.Status()
    time.sleep(10)
    s.close()


