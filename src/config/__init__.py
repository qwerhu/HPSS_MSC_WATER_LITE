# coding=utf-8
"""
通过api获取配置数据
"""
import logging
import requests
import simplejson
import ctx
from data import RedisCache

CONFIG_API_DATA = RedisCache('config_data')
temp_cache = {}


def load(base_url, config_name):
    global temp_cache
    url = base_url + 'GetConfigByName?name=%s' % config_name
    r = requests.get(url)
    o = r.json()
    if isinstance(o, str):
        o = simplejson.loads(o)
    if o is not None:
        # 缓存
        # CONFIG_API_DATA.set(config_name, o)
        temp_cache[config_name] = o
    else:
        logging.error('[%s] load config data failed' % config_name)
    return o


def get(name):
    # o = CONFIG_API_DATA.get(name)
    o = temp_cache.get(name)
    if not o:
        o = load(ctx.config_api_url, name)
    return o
