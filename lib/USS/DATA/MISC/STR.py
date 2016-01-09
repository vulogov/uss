__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring

