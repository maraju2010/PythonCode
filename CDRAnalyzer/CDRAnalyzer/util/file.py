"""
    functions to read and write entries from settings.cache.txt.
"""
import os
import inspect
import sys
import pickle
from functools import reduce

class filepath(object):

    def get_filepath(self):
        try:
            filename = __file__
        except NameError:
            filename = inspect.getsourcefile(get_filepath)
        return os.path.realpath(filename)

    def  write_file(self,data):
        curr_path = self.get_filepath()
        cache_path = reduce(lambda x,f: f(x),[os.path.dirname]*2, curr_path)
        cache = os.path.join(cache_path, "settings", "cache.txt")
        with open(cache,"wb") as filehandle:
                pickle.dump(data,filehandle)

    def read_file(self):
        curr_path = self.get_filepath()
        cache_path = reduce(lambda x,f: f(x),[os.path.dirname]*2, curr_path)
        cache = os.path.join(cache_path, "settings", "cache.txt")
        with open(cache,"rb") as filehandle:
            cachelist = pickle.load(filehandle)
        return cachelist
