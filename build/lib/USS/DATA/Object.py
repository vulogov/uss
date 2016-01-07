__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class Object(object):
    def Object__set_attr(self, key, argv):
        if argv.has_key(key):
            setattr(self, key, argv[key])


