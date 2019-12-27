#!/user/bin/python3
# -*- coding: utf-8 -*-

"""
@Author: ChenHanping
@Email:
@QQ:

@date: 2019/12/3
@description:
"""
import json
import copy
from datetime import datetime,timedelta
import ctx
# from src import ctx
from service.handlers.base import BaseHandler
from utils import api_util

def _db():
    return ctx.modledb['model_result_simulation']

def tt(date):
    #datetime转换为字符串T%H%M
    at = ((date.minute) // 15) * 15
    if at==0:
        at='00'
    t = date.strftime('T%H')+str(at)
    return t

def conversion(target1,date,t,staTime,endTime):
    DATA = {}
    res = []
    # 预测数据
    for target in target1:
        statusYC = {'TARGET_ID': target, 'DATA_DATE': date, 'DATA_TYPE': 1, 'SCADATYPE': 5}
        frequencyYC = {'TARGET_ID': target, 'DATA_DATE': date, 'DATA_TYPE': 1, 'SCADATYPE': 7}
        if target == 'PMP-1':
            for v in _db().find_one(frequencyYC, {'_id': 0, t: 1}).values():
                for i in v:
                    if i['time'] < endTime:
                        DATA['id'] = target
                        DATA['time'] = i['time']
                        DATA['status'] = i['status']
                        DATA['frequency'] = i['frequency']
                        Date = copy.copy(DATA)
                        res.append(Date)
        else:
            for a in _db().find_one(statusYC, {'_id': 0, t: 1}).values():
                for i in a:
                    if i['time'] < endTime:
                        DATA['id'] = target
                        DATA['time'] = i['time']
                        DATA['status'] = i['status']
                        DATA['frequency'] = i['frequency']
                        Date = copy.copy(DATA)
                        res.append(Date)
    # 回算数据
    for target in target1:
        statusHS = {'TARGET_ID': target, 'DATA_DATE': date, 'DATA_TYPE': 0, 'SCADATYPE': 5}
        # frequencyHS = {'TARGET_ID': target, 'DATA_DATE': date, 'DATA_TYPE': 0, 'SCADATYPE': 7}
        for v in _db().find_one(statusHS, {'_id': 0, t: 1}).values():
            res2 = [m for m in v]
            res2.sort(key=lambda x: x['time'], reverse=True)
            for m in res2:
                DATA['id'] = target
                DATA['time'] = m['time']
                DATA['status'] = m['status']
                if DATA['time'] < staTime:
                    DATA['time'] = staTime + " 00:00:00"
                    Date = copy.copy(DATA)
                    res.append(Date)
                    break
                Date = copy.copy(DATA)
                res.append(Date)
    # 排序
    res.sort(key=lambda x: x['time'])
    return res

class SchHadl(BaseHandler):
    async def get(self):
        # 获取编号
        target = self.get_argument('target_id', None)
        if not target:
            self.return_failed()
            return
        target1 = target.split(',')
        #获取时间，时间为空用当前时间
        newTime = self.get_argument('new_time', None)
        if not newTime:
            NTime = datetime.now()
        else:
            NTime = datetime.strptime(newTime, "%Y-%m-%d %H:%M:%S")
        t = tt(NTime)
        #获取日期
        date = NTime.strftime('%Y%m%d')
        #开始时间，结束时间
        staTime = NTime.strftime('%Y-%m-%d')
        endTime = (NTime+timedelta(days=1)).strftime('%Y-%m-%d')
        result = await api_util.call_blocking(conversion, target1,date,t,staTime,endTime)
        self.write(json.dumps(result, ensure_ascii=False))




