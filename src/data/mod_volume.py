import time
from datetime import datetime
import pymongo
import ctx
import re

COLLECTION_NAME = 'model_result_volume'
# 间隔时间，单位秒
INTERVAL = 15 * 60
FORMAT_DATA_DATE = '%Y%m%d'
FORMAT_TIME_TAG = 'T%H%M'
# 时间标签模板
TIME_TAG_TEMPLATE = [time.strftime(FORMAT_TIME_TAG, time.localtime(x)) for x in range(0, 86400 + INTERVAL, INTERVAL)]


def _db():
    return ctx.modledb[COLLECTION_NAME]


def _get_timestamp(_time):
    if _time is None:
        return None
    if isinstance(_time, time.struct_time):
        return time.mktime(_time)
    elif isinstance(_time, datetime):
        return time.mktime(_time.timetuple())
    return _time


def _upsert(filters, add_data, update_data):
    collection = _db()
    data = collection.find(filters)
    if data.count() == 0:
        collection.insert_one(add_data)
    else:
        # id = str(data[0]["_id"])
        # update_data["_id"] = id
        collection.update_one(filters, {"$set": update_data})


def upsert(target_id, _time, data_type, scada_type, data):
    time_tag = _time.strftime(FORMAT_TIME_TAG)
    add_data = dict()
    add_data['DATA_DATE'] = _time.strftime(FORMAT_DATA_DATE)
    add_data['TARGET_ID'] = target_id
    add_data['DATA_TYPE'] = data_type
    add_data[time_tag] = data
    add_data['SCADATYPE'] = scada_type

    update_data = {time_tag: data}
    filter_list = list()
    filter_list.append({"TARGET_ID": {"$eq": target_id}})
    filter_list.append({"DATA_TYPE": {"$eq": data_type}})
    filter_list.append({"SCADATYPE": {"$eq": scada_type}})
    filter_list.append({"DATA_DATE": {"$eq": _time.strftime(FORMAT_DATA_DATE)}})
    filters = {"$and": filter_list}
    _upsert(filters, add_data, update_data)


def items(s, e, ids=None, data_type=None, sort=[('TARGET_ID', 1), ('TIME', 1)]):
    # 转换为时间戳
    if isinstance(s, time.struct_time):
        s = time.mktime(s)
        e = time.mktime(e)
    elif isinstance(s, datetime):
        s = time.mktime(s.timetuple())
        ji = type(s)
        print(ji)
        e = time.mktime(e.timetuple())
    # 对齐
    s = s + (INTERVAL - s % INTERVAL)
    print('====='*20)
    print(s)
    e = e - e % INTERVAL
    print('====='*30)
    print(e)
    # 开始和结束日期字符串
    s_day = time.strftime(FORMAT_DATA_DATE, time.localtime(s))
    e_day = time.strftime(FORMAT_DATA_DATE, time.localtime(e))
    # 时分标识的数组
    time_list = range(int(s), int(e + INTERVAL), INTERVAL)
    time_tags = [time.strftime(FORMAT_DATA_DATE + FORMAT_TIME_TAG, time.localtime(x)) for x in time_list]
    q = {
        'DATA_TYPE': int(data_type),
        'DATA_DATE': {'$gte': s_day, '$lte': e_day}
    }
    if ids is not None and len(ids) > 0:
        q['TARGET_ID'] = {'$in': ids}
    print(ids)
    print(q)
    if data_type is not None:
        q['DATA_TYPE'] = data_type
    r = []
    ko = _db().find(q).sort([('DATA_DATE', 1)]).limit(10)
    for i in ko:
        print(i)
    print(ko)
    for o in _db().find(q).sort([('DATA_DATE', 1)]):
        o_id = o['TARGET_ID']
        o_d_type = o['DATA_TYPE']
        o_date = o['DATA_DATE']
        for tag in TIME_TAG_TEMPLATE:
            temp_tag = o_date + tag
            try:
                o_data = o[tag]
            except:
                continue
            # if o_data is None:
            #     continue
            if temp_tag in time_tags:
                r.append({'TARGET_ID': o_id, 'DATA_TYPE': o_d_type,
                          'TIME': time.strptime(temp_tag,FORMAT_DATA_DATE + FORMAT_TIME_TAG),
                          'DATA': o_data})
    sort = dict(sort)
    r.sort(key=lambda x: (sort['TARGET_ID'] * x['TARGET_ID'], sort['TIME'] * x['TIME']))
    print('i am a ',r)
    return r


def item_raw(target_id=None, data_type=None, date=None):
    """
    获取原始记录
    :param target_id:
    :param data_type:
    :param date:
    :return:
    """
    q = {}
    if target_id is not None:
        q['TARGET_ID'] = target_id
    if data_type is not None:
        q['DATA_TYPE'] = int(data_type)
    if date is not None:
        q['DATA_DATE'] = date
    if q == {}:
        return None
    res = []
    for o in _db().find(q):
        # delete _id
        o.pop('_id', None)
        # 为了兼容旧格式（前端用）的特殊处理
        o_d_type = o['DATA_TYPE']
        o_date = o['DATA_DATE']
        if o_d_type != 0:
            for k in o.keys():
                if re.match('T\\d', k) is not None:
                    t = time.strptime(o_date + k, FORMAT_DATA_DATE + FORMAT_TIME_TAG)
                    step = ctx.pattern_step / 60
                    e = time.localtime(time.mktime(t) + ctx.duration)
                    o[k] = {
                        'Data': o[k],
                        'Stime': time.strftime('%Y-%m-%d %H:%M:%S', t),
                        'Etime': time.strftime('%Y-%m-%d %H:%M:%S', e),
                        'Steptime': step
                    }
        res.append(o)
    return res


def last(target_id, data_type, _time=None):
    pass


def one(target_id, _time, data_type):
    result = None
    date_tag = _time.strftime(FORMAT_TIME_TAG)
    filter_list = list()
    filter_list.append({"TARGET_ID": {"$eq": target_id}})
    filter_list.append({"DATA_TYPE": {"$eq": data_type}})
    filter_list.append({"DATA_DATE": {"$eq": _time.strftime(FORMAT_DATA_DATE)}})
    filters = {"$and": filter_list}
    data_list = _db().find(filters, sort=[("DATA_DATE", pymongo.ASCENDING)])
    if data_list.count() > 0:
        data = data_list[0]
        if date_tag in data:
            result = data[date_tag]

    return result


def count_by_time(s, e, data_type, scadatype):
    """根据开始和结束时间日期计算数量"""
    start_day = datetime.strftime(s, FORMAT_DATA_DATE)
    end_day = datetime.strftime(e, FORMAT_DATA_DATE)
    q = {
        'DATA_TYPE': int(data_type),
        'SCADATYPE': int(scadatype),
        'DATA_DATE': {'$gte': start_day, '$lte': end_day}
    }
    count = len(_db().find(q).distinct('DATA_DATE'))
    return count
