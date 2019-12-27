# -*- coding:utf-8 -*-
from functools import wraps

def singleton(cls):
    instance = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]
    return getinstance

@singleton
class cachestore(object):
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key, df=None):
        return self.cache.get(key, df)