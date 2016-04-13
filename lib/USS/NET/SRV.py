__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'


import SocketServer
import socket
import multiprocessing
from multiprocessing.reduction import reduce_handle
from USS.ENV.ENV import main

env = main("../../../etc")
env.clips.PrintFacts()

class TCP_SERVER:
    def __init__(self):
        pass

