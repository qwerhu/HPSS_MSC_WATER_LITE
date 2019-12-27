import re
import ctx
import time
from datetime import datetime
from collections import defaultdict
from enum import Enum
# from hyd.realtime.enums import SimuResultType, OnlineType

COLLECTION_NAME = 'model_result_simulation'
# 间隔时间，单位秒
INTERVAL = 15 * 60
FORMAT_DATA_DATE = '%Y%m%d'
FORMAT_TIME_TAG = 'T%H%M'
# 时间标签模板
TIME_TAG_TEMPLATE = [time.strftime(FORMAT_TIME_TAG, time.localtime(x)) for x in range(0, 86400, INTERVAL)]
# print(time.strftime(FORMAT_TIME_TAG, time.localtime(0)))
# print(TIME_TAG_TEMPLATE)
# print(time.localtime(0))
# print(time.localtime())

class TargetType(Enum):
    PRESS = 0
    FLOW = 1


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
        collection.update_one(filters, {"$set": update_data})


def upsert(target_id, _time, data_type, scada_type, data):
    scada_type = int(scada_type)
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


def items(s, e, ids=None, data_type=None, target_type=None, sort=[('TARGET_ID', 1), ('TIME', 1)]):
    # 转换为时间戳
    if isinstance(s, time.struct_time):
        s = time.mktime(s)
        e = time.mktime(e)
    elif isinstance(s, datetime):
        s = time.mktime(s.timetuple())
        e = time.mktime(e.timetuple())
    # 对齐
    s = (s + (INTERVAL - s % INTERVAL)) if (s % INTERVAL) != 0 else s
    e = e - e % INTERVAL
    # 开始和结束日期字符串
    s_day = time.strftime(FORMAT_DATA_DATE, time.localtime(s))
    e_day = time.strftime(FORMAT_DATA_DATE, time.localtime(e))
    # 时分标识的数组
    time_list = range(int(s), int(e + INTERVAL), INTERVAL)
    time_tags = [time.strftime(FORMAT_DATA_DATE + FORMAT_TIME_TAG, time.localtime(x)) for x in time_list]
    q = {
        'DATA_DATE': {'$gte': s_day, '$lte': e_day}
    }
    if ids is not None and len(ids) > 0:
        q['TARGET_ID'] = {'$in': ids}
    if data_type is not None:
        q['DATA_TYPE'] = int(data_type)
    if target_type is not None:
        q['SCADATYPE'] = int(target_type)
    r = []
    for o in _db().find(q).sort([('DATA_DATE', 1)]).limit(50):
        o_id = o['TARGET_ID']
        o_t_type = o['SCADATYPE']
        o_d_type = o['DATA_TYPE']
        o_date = o['DATA_DATE']
        for tag in TIME_TAG_TEMPLATE:
            temp_tag = o_date + tag
            o_data = o.get(tag)
            if o_data is None:
                continue
            if temp_tag in time_tags:
                r.append({'TARGET_ID': o_id, 'SCADATYPE': o_t_type, 'DATA_TYPE': o_d_type,
                          'TIME': time.strptime(temp_tag, FORMAT_DATA_DATE + FORMAT_TIME_TAG),
                          'DATA': o_data})

    sort = dict(sort)
    r.sort(key=lambda x: (sort['TARGET_ID'] * x['TARGET_ID'], sort['TIME'] * x['TIME']))
    return r


def item_raw(target_id=None, target_type=None, data_type=None, date=None):

    """
    获取原始记录
    :param target_id:
    :param target_type:
    :param data_type:
    :param date:
    :return:
    """

    q = {}
    if target_id is not None:
        q['TARGET_ID'] = target_id
    if target_type is not None:
        q['SCADATYPE'] = int(target_type)
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
        t_type = int(o.get('SCADATYPE', -1))
        o['TARGET_TYPE'] = t_type
        # 为了兼容旧格式（前端用）的特殊处理
        if t_type in [SimuResultType.PRESS.value, SimuResultType.FLOW.value, SimuResultType.WATER_LEVEL.value,
                      SimuResultType.PUMP_ENERGY.value]:
            for k in o.keys():
                if re.match('T\\d', k) is not None:
                    oo = o[k]
                    o[k] = dict(
                        ((k.capitalize() if k not in ['tagname', 'id'] else k.upper()), v) for k, v in oo.items())
        elif t_type in [SimuResultType.PUMP_OPERATION.value, SimuResultType.PUMP_FREQUENCY.value]:
            # 泵的操作模拟结果
            for k in o.keys():
                if re.match('T\\d', k) is not None:
                    oo = o[k]
                    if oo is not None and len(oo) > 0:
                        o[k] = [{'S': x.get('status', ''), 'T': x.get('time', ''), 'F': x.get('frequency', '')} for x in
                                oo]
        elif t_type in [SimuResultType.WATER_REPORT]:
            for k in o.keys():
                if re.match('T\\d', k) is not None:
                    oo = o[k]
                    if oo is not None and len(oo) > 0:
                        o[k] = [{'YSTOTAL': x['ystotal'], 'CCSTOTAL': x['ccstotal'], 'YHTOTAL': x['yhtotal'],
                                 'TXTOTAL': x['txtotal']} for x in oo]
        res.append(o)
    return res


def last(target_id, data_type, _time=None):
    pass


def get_obj_str(obj):
    """
    :param obj: 对象
    :return: 构建好的对象字符串
    """
    if hasattr(obj, '__dict__'):
        return {k: get_obj_str(v) for k, v in obj.__dict__.items()}
    elif hasattr(obj, '__slots__'):
        return {i: get_obj_str(getattr(obj, i, '')) for i in obj.__slots__}
    elif isinstance(obj, list):
        return [get_obj_str(i) for i in obj]
    else:
        return obj


def get_result_str(result):
    """
    将结果转为字符串
    @note: 特殊情况：压力报表 嵌套列表
    :param result:
    :return:
    """
    if isinstance(result, str):
        result_string = result
    elif isinstance(result, list):
        result_string = [get_result_str(r) for r in result]
    else:
        result_string = get_obj_str(result)

    return result_string


def save_simulate_result(date_time, model_type, ptype, target_id, result, flag=False):
    """
    :param date_time: 模型分析的日期时间
    :param model_type: 回算或者预测
    :param ptype: 结果类型
    :param target_id: ID
    :param result: 结果
    :param flag: 是否直接存结果
    :return:
    """

    data_type = model_type.value
    if flag:
        result_string = result
    else:
        result_string = get_result_str(result)

    upsert(target_id, date_time, data_type, ptype, result_string)


def max_min_press(s, e, data_type, scada_type, target_id):
    start_day = datetime.strftime(s, FORMAT_DATA_DATE)
    end_day = datetime.strftime(e, FORMAT_DATA_DATE)
    q = {
        'DATA_TYPE': int(data_type),
        'SCADATYPE': scada_type,
        'DATA_DATE': {'$gte': start_day, '$lte': end_day},
        'TARGET_ID': target_id
    }
    result = _db().find(q)
    days_dict = defaultdict(list)
    for press_dict in result:
        press_list = press_dict['T0000']
        for index, data in enumerate(press_list):
            days_dict[index].extend(data)

    max_min_dict = defaultdict(lambda: [[], []])
    for day in list(range(1, 24)) + [0]:
        all_data = days_dict[day]
        dma_max_dict, dma_min_dict = dict(), dict()
        for dma_data in all_data:
            id_, value = dma_data['ID'], dma_data['VALUE']
            if id_ not in dma_max_dict:
                dma_max_dict[id_] = value
            elif value > dma_max_dict[id_]:
                dma_max_dict[id_] = value

            if id_ not in dma_min_dict:
                dma_min_dict[id_] = value
            elif value < dma_min_dict[id_]:
                dma_min_dict[id_] = value

        for dma_id, max_value in dma_max_dict.items():
            max_min_dict[dma_id][0].append(max_value)

        for dma_id_, min_value in dma_min_dict.items():
            max_min_dict[dma_id_][1].append(min_value)

    return max_min_dict
