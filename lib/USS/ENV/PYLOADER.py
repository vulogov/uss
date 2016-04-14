__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import imp
import types
from FS import *

class PYLOADER:
    def __init__(self):
        self.mods = {}
    def module_loaded(self, mod, fun):
        pass
    def mod_exec(self, _mod):
        if type(_mod) == types.StringType:
            ## Passing the name
            _mod = self.find_the_mod(_mod)
            if _mod == None:
                return []
        elif type(_mod) == types.ModuleType:
            _mod = _mod
        else:
            return []
        out = []
        for f in dir(_mod):
            if type(getattr(_mod, f)) != types.FunctionType:
                continue
            out.append(f)
        return out
    def find_the_mod(self, mod_name):
        for p in self.mods.keys():
            if self.mods[p].has_key(mod_name):
                return self.mods[p][mod_name]
        return None
    def reload_mods(self):
        for p in self.path:
            if not self.mods.has_key(p):
                self.mods[p] = {}
            dir = get_dir_content(p)
            for m in dir:
                file, full_path, mod = m
                modname, ext = mod
                if ext not in [".py",] or self.find_the_mod(modname) != None:
                    continue
                try:
                    _mod = imp.load_source(modname, full_path)

                except:
                    continue
                self.mods[p][modname] = _mod
                f_list = self.mod_exec(_mod)
                for f in f_list:
                    self.module_loaded(modname, f)
        for p in self.mods.keys():
            if p not in self.path:
                del self.mods[p]
