__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class PYEXEC:
    def __call__(self, modname, *args, **kw):
        parse = modname.split(".")
        if len(parse) == 1:
            _mod     = modname
            _fun     = "main"
        elif len(parse) >= 2:
            _mod = parse[0]
            _fun = parse[1]
        else:
            raise ValueError, "Bad function name %s"%modname
        mod = self.find_the_mod(_mod)
        if mod == None:
            raise ValueError, "Module %s not found"%modname
        try:
            fun = getattr(mod, _fun)
        except:
            raise ValueError, "Function %s.%s not exists"%(_mod, _fun)
        try:
            return apply(fun, args, kw)
        except:
            raise ValueError, "Error in %s.%s"%(_mod, _fun)
