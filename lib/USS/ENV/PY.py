__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from FS import *
from PYLOADER import PYLOADER
from PYEXEC import PYEXEC
from USS.DATA.Object import Object

class PY(Object, PYLOADER, PYEXEC):
    def __init__(self, *path):
        self.path = []
        print path
        for d in list(path):
            if check_directory(d):
                self.path.append(d)
        PYLOADER.__init__(self)
        self.reload_mods()
    def __add__(self, path):
        if not check_directory(path) or path in self.path:
            return self
        self.path.append(path)
        return self
    def __sub__(self, path):
        if path in self.path:
           self.path.remove(path)
        return self

if __name__ == '__main__':
    p = PY("../../../etc/ini/py")
    print p("dummy.main")
    print p.execute("main")