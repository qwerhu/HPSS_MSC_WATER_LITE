"""
全局变量
"""
import os
import time
# import time
import threading
from redis import StrictRedis
from db.oracle import Oracle
from db import encrypt
from utils.config_util import Config
from pymongo.mongo_client import MongoClient
from utils.log import HpLog
from common.msgqueue import RedisQueue

# 全局的epanet的使用锁
glock = threading.Lock()
# 获取本地配置文件
config_path = os.path.dirname(os.path.abspath(__file__)) + '\\config\\config.json'
config = Config(config_path)
config_api_url = config.get('config', 'url')
# mongodb config
app_name = config.get('sys', 'app_name')
cwd = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cwd, config.get('config', 'data_path')))
# base_path = os.path.abspath(config.get('config', 'data_path'))
# shape模板文件所在的目录
shp_template_path = os.path.join(base_path, 'template')
# 节点shape文件的名称
shp_name_node = config.get('config', 'node_shp')
# 线shape文件的名称
shp_name_link = config.get('config', 'link_shp')
# 水厂模式
is_plant_mode = config.get('config', 'is_simple_mode', 'false') == 'true'
# redis 配置
_redisinfo = config.get('sys', 'redis')
MSG_REPORT = 'MSG_REPORT'
MSG_MODEL_CACHE_UPDATE = 'msg_model_cache_update'
_queue_prefix = 'RMQ' + (':' + app_name if app_name else '')
msg_queue = RedisQueue(_redisinfo, _queue_prefix)
# 相互引用，bus 必须在msg_queue声明之后
from common.bus import Bus
bus = Bus

# 模型计算相关配置
QSecond = config.get('config', 'QSecond', 3600)  # 水质分析的时间间隔(秒)
QDuration = config.get('config', 'QDuration', 432000)  # 水质分析持续时间(秒)
global_pattern_id = 'Globalpattern_0122'
pattern_step = config.get('config', 'hyd_step', 5 * 60)
result_step = config.get('config', 'result_step', 30 * 60)  # 写json文件间隔
result_interval = int(result_step / pattern_step)
hour_pattern_count = int(3600 / pattern_step)  # 一个小时内结果数目
day_pattern_count = int(86400 / pattern_step)  # 一天内结果数目
online_compute_step = config.get('config', 'online_compute_step', 15 * 60)
duration = config.get('config', 'm_duration', 86400)
m_SRID = config.get('config', 'SRID', 300002)
m_buff_dis = config.get('config', 'buff_dis', 20)
set_type = config.get('config', 'SetType', 1)  # 阀门关闭设置类型,1代表线，0代表点
waterpath_alarm = config.get('config', 'waterpath_alarm', 4)
pressalarm_days = config.get('config', 'pressalarm_days', 7)
# 坐标是否是经纬度的
is_wgs84 = config.get('config', 'is_wgs84', 'false') == 'true'
# 泵的连续操作最短时间阈值，低于该阈值的操作忽略，0表示无限制
pump_opt_time_limit = 0
# 需水量及需水量模式计算修正系数的采样数量
forecast_rectify = 24
# 校正系数人工设置上下限，避免出现异常系数
coff_max = 1.05
coff_min = 0.95
# 工作日前算天数
weekdaypre = 3
# 休息日前算天数
weekendpre = 2
# 压力分区预警天数
pressalarmdays = 7
# demo 日期，当无scada历史数据时可启用此配置，取指定日期的历史数据
demo_date = config.get('config', 'demo_date')
# 转成时间戳
if demo_date:
    demo_date = time.mktime(time.strptime(demo_date, '%Y-%m-%d'))

_queue_prefix = 'RMQ' + (':' + app_name if app_name else '')

_mongoinfo = config.get('sys', 'mongodb')
# 解密
if _mongoinfo is not None and 'password' in _mongoinfo and _mongoinfo.get('password'):
    _mongoinfo['password'] = encrypt.decode(str(_mongoinfo.get('password')))
mongodb = MongoClient(maxPoolSize=config.get('sys', 'maxPoolSize', 128), connect=False, **_mongoinfo)
# 检查mongodb连接
# while True:
#     try:
#         print('test connect to mongodb...')
#         mongodb['test']['__test__'].count()
#         print('pass')
#         break
#     except KeyboardInterrupt:
#         print('Terminated!')
#         break
#     except:
#         print('unable to connect ' + str(config.get('sys', 'mongodb')))
#         print('reconnecting')
#     time.sleep(2000)

# Oracle db config


# zlsdb
_zlsdbinfo = config.get('sys', 'zlsdb')
zlsdb = Oracle.getDB(**_zlsdbinfo)
# 模型结果库
modledb = mongodb['modeldb']
hmdb = mongodb['scadadb_history']
rmdb = mongodb['scadadb_real']
# 实例化Redis
redis_db = StrictRedis.from_url(_redisinfo)

NEW_BUCKET = config.get('sys', 'nb', True)
# api 端口
api_port = config.get('config', 'api_port', 25096)

# 日志文件
logger = HpLog()

# 九鼎接口地址
JDInterfaceUrl = 'http://182.150.63.195:17346/jdrx-ba-pumps-huiji/system/0/ba/pumps/pumpGroup/query'
