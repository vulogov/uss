__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'


class TEMPLATE:
    def __init__(self, *args, **kw):
        self.args = args
        self.kw   = kw
        self._searchDirectories()
    def _searchDirectories(self):
        if not self.kw.has_key("templatePath") or type(self.kw["templatePath"]) != type([]) or len(self.kw["templatePath"]) == 0:
            raise ValueError, "templatePath value is incorrect"
