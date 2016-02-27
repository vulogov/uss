__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from PYCLP import PYCLP

class ENV(PYCLP):
    def __init__(self, **argv):
        self.Object__set_attr("path", self.argv)
        apply(PYCLP.__init__, (self,), argv)


