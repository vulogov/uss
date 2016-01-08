__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class LOADER:
    def _load(self, lf_file, lf_string, args):
        if args.has_key("file") and lf_file:
            return apply(lf_file, (args["file"],))
        elif args.has_key("data") and lf_string:
            return apply(lf_string, (args["data"],))
        else:
            raise ValueError, "Loader requested to load not from file, nether from string"

