import ctx
import logging
import time
import pandas as pd
from aenum import Enum, NoAlias
from data import historycl
from datetime import datetime, timedelta
from os import path
from db import oracle
from epanet.toolkit import toolkit as en
from epanet.output import output as oapi
from utils.date_util import HOLIDAYS
from utils.dma_util import zbid2sid_list
import traceback


class ModelScadaType(Enum):
    _settings_ = NoAlias
    TANK = 2
    PUMP = 4
    YUAN_SHUI = 0
    CHU_CHANG_SHUI = 1
    ALL_FLOW = 1
    PRESS = 0
    VIP_CUSTOMER = 3
    PUMP_FREQUENCY = 5


def align_online_time(target_date):
    """
    对准在线计算的步长时间
    :param target_date: 需要对准的时间，datetime, time, timestamp都支持
    :return: 返回对准后的时间戳
    """
    if isinstance(target_date, datetime):
        t = target_date.timestamp()
    elif isinstance(target_date, time.struct_time):
        t = time.mktime(target_date)
    elif isinstance(target_date, int) or isinstance(target_date, float):
        t = target_date
    else:
        raise Exception('不支持的参数类型')
    return t - (t - time.timezone) % ctx.online_compute_step


def get_vip_customers(model_name=None):
    """
    获取大用户信息，包括pattern
    :param model_name:
    :return:
    """
    sql = 'select * from v_model_water order by sort'
    cus_list = oracle.query(ctx.zlsdb, sql)
    if model_name is not None:
        p = get_inp_path(model_name)
        if path.exists(p):
            with ctx.glock:
                ph = en.proj_create()
                try:
                    en.proj_open(ph, p, '', '')
                    for c in cus_list:
                        c_id = c.get('ID')
                        m_index = en.node_getindex(ph, c_id)
                        ptn = en.node_getvalue(ph, m_index, en.NodeProperty.PATTERN)
                        c['PATTERN'] = ptn
                        patter_id = en.ptrn_getid(ph, int(ptn))
                        c['PATTERN_ID'] = patter_id
                except Exception as err:
                    msg = '在模型%s中查询pattern出错：%s' % (model_name, str(err))
                    ctx.logger.log_status(msg, 4)
                    logging.error(msg)
                finally:
                    en.proj_close(ph)
                    en.proj_delete(ph)
    return cus_list


def get_pumps_info():
    """
    获取水泵tagname与其模型id的对应字典
    :return:
    """
    sql = "select * from v_model_pump where target_type = '4'"
    p_list = oracle.query(ctx.zlsdb, sql)
    return {x['TAGNAME']: x['ID'] for x in p_list}


def get_other_customer(mean_other):
    """
    获取一般用户的信息（有在模型中分配水量的）
    为了避免百分比值过小导致精确为了，将水量放在SQL中进行计算
    :param mean_other: 其他用户的总水量
    :return:
    """
    sql = "select id,round(percent*{}/3.6,4) as demand from MODEL_RELATION t where sblb like '%YH%' and percent is not null".format(
        mean_other)
    cus_list = oracle.query(ctx.zlsdb, sql)
    return cus_list


def get_inp_path(model_name):
    """
    获取模型文件路径
    :param model_name: 模型名称
    :return: 模型文件的路径
    """
    return path.join(ctx.base_path, model_name + '.inp')


def get_flow_info(_type):
    """
    获取流量(原水、出厂水)的scada指标与模型id对应的字典
    :param _type: 流量类型 原水0，出厂水1
    :return:
    """
    sql = "select * from V_MODEL_FLOW t where scadatype = %s" % _type
    f_list = oracle.query(ctx.zlsdb, sql)
    return {x['TAGNAME']: x['ID'] for x in f_list}


def get_other_pattern():
    """
    查询大用户以外的Pattern
    :return:
    """
    sql = "select patternid,patternvalue from model_patterns"
    p_list = oracle.query(ctx.zlsdb, sql)
    return {x['PATTERNID']: x['PATTERNVALUE'] for x in p_list}


def get_model_scada(_type):
    """
    获取scada的tagname与模型id的对应关系
    :param _type: ModelScadaType.xxx
    :return:
    """
    if not isinstance(_type, Enum):
        raise Exception('错误的参数，要求是ModelScadaType的枚举')
    if _type in [ModelScadaType.YUAN_SHUI, ModelScadaType.CHU_CHANG_SHUI]:
        w = 'scadatype = %s' % _type.value
    else:
        w = 'target_type = %s' % _type.value
    sql = "select * from v_model_scada where %s" % w
    r_list = oracle.query(ctx.zlsdb, sql)
    return {x['TAGNAME']: x['ID'] for x in r_list}


def get_his_times(target_date):
    """
    获取指定日期历史采样时间段的开始和结束时间戳
    :param target_date:
    :return:
    """
    today = target_date
    tomorrow = today + timedelta(days=1)
    t_today = HOLIDAYS.get_day_type(today)
    t_tomorrow = HOLIDAYS.get_day_type(tomorrow)
    if t_today == t_tomorrow:
        days = 5 if HOLIDAYS.is_holiday(today) else 10
        date_list = HOLIDAYS.get_same_days(days, t_today, today)
        result = (date_list[0], date_list[days - 1])
    else:
        t_days = 5 if HOLIDAYS.is_holiday(today) else 10
        t_date_list = HOLIDAYS.get_same_days(t_days, t_today, today)
        m_days = 5 if HOLIDAYS.is_holiday(tomorrow) else 10
        m_date_list = HOLIDAYS.get_same_days(m_days, t_tomorrow, tomorrow)
        result = (min(t_date_list[0], m_date_list[0]), max(t_date_list[t_days - 1], m_date_list[m_days - 1]))
    s = time.mktime(result[0].timetuple())
    s = s - (s - time.timezone) % 86400
    e = time.mktime(result[1].timetuple())
    e = e + (86400 - (s - time.timezone) % 86400) - 1
    return s, e


def get_scada_data(sids, s, e ,filter = True):
    """
    获取按照模型分析步长抽稀过的SCADA数据
    :param sids:ItemName可以为多个
    :param s: 开始时间
    :param e: 结束时间
    :param filter: 是否按照Pattern步长处理数据，默认为处理
    :return:
    """
    zids = zbid2sid_list(sids)
    _data = historycl.items(s, e, Ids=zids)
    if len(_data) > 0:
        df = pd.DataFrame(_data)
        df.index = df['time']
        if filter:
            # 抽稀数据，匹配pattern的步长
            df = df[df['time'] % ctx.pattern_step == 0]
        df['value'] = df['value'].astype(float)
        return df
    return


def get_model_data(model_name, model_ids, element_type, time_idx, property):
    """
    根据传入的模型ID获取特定时刻的某一种模型分析结果
    :param model_name: 模型名称
    :param mode_ids: 模型ID
    :param obj_type: 模型对象类型 oapi.ElementType
    :param time_idx: 时间序号
    :param property: en.NodeProperty en.LinkProperty
    :return:
    """
    file_out = path.join(ctx.base_path, model_name + '.out')
    if not path.exists(file_out):
        raise Exception(u'out file not exist: %s' % file_out)
    hd = oapi.init()
    oapi.open(hd, file_out)
    size_list = oapi.getnetsize(hd)  # nodes, tanks, links, pumps, valves
    if element_type == oapi.ElementType.NODE:
        num_objs = size_list[0]
    elif element_type == oapi.ElementType.LINK:
        num_objs = size_list[2]
    index_objs = range(1, num_objs + 1, 1)
    obj_dict = {}
    for index in range(1, num_objs + 1):
        _id = oapi.getelementname(hd, element_type, int(index)).rstrip('\x00')
        if _id in model_ids:
            obj_dict[_id] = index
        if len(obj_dict) == len(model_ids):
            break
    value_dict = {}
    for _id in obj_dict:
        r = oapi.getnoderesult(hd, time_idx, obj_dict[_id])
        value_dict[_id] = r[property.value]  # modify
    oapi.close(hd)
    return value_dict


def get_model_userinfo():
    """
    获取模型用户信息, 计算用户水量
    :return:
    """
    user_info = {}
    sql = "select ID,GJZ from model_relation t where sblb like '%YH%' and hm is not null "
    try:
        res_list = oracle.query(ctx.zlsdb, sql)
        for dic in res_list:
            id_ = str(dic['ID']) if 'ID' in dic else ''
            gjz = str(dic['GJZ']) if 'GJZ' in dic else ''
            user_info[id_] = gjz
    except Exception as ex:
        ctx.logger.log_status(ex)
    return user_info


def update_model_template(service_name, start_time, time_step, time_range):
    """
    @note: 更新模型运行状况，便于前端展示
    :param service_name: 服务名称
    :param start_time: 开始运行时间
    :param time_step: 步长
    :param time_range: 分析持续时间
    :return:
    """
    if service_name == '':
        sql = "update MODEL_MAP_TEMPLATE set stime='" + start_time + "' where caltype != 0 and type = 0"
    else:
        sql = "update MODEL_MAP_TEMPLATE set lastcal = sysdate ,stime='" + start_time + "',time_step='" + time_step + "',time_range='" + time_range + "' where layer_name ='" + service_name + "'"
    try:
        result = oracle.execute(ctx.zlsdb, sql)
    except Exception as ex:
        ctx.logger.log_status(ex)
        traceback.print_exc()


def get_pipeline_ids(path_id=""):
    """
    :param path_id: 管线id
    :return: 模型id
    """
    if len(path_id) == 0:
        sql = "select distinct modelid from model_waterpath_detail"
    else:
        wheresql = ""
        for index, id_ in enumerate(path_id):
            if index == 0:
                wheresql += "'{}'".format(id_)
            else:
                wheresql += ",'{}'".format(id_)
        sql = "select distinct modelid from model_waterpath_detail t where pathid in ({})".format(wheresql)
    result = oracle.fetch_all(ctx.zlsdb, sql)
    return result


def get_model_valvecount():
    """
    获取模型中设置的阀门的数量
    :return:
    """
    cnt = 0
    sql = "select count(*) CNT from v_model_valve"
    result = oracle.query(ctx.zlsdb, sql)
    if result:
        cnt = result[0].get('CNT', 0)

    return cnt


def get_patterns(ph):
    """
    获取模型内所有的pattern
    :param ph:
    :return:
    """
    patterns_dict = dict()
    len_patterns = en.rprt_getcount(ph, en.CountType.PTRNS)
    for i in range(1, len_patterns + 1):
        id_ = en.ptrn_getid(ph, i)
        ptrn_len = en.ptrn_getlength(ph, i)
        patterns = []
        for j in range(1, ptrn_len + 1):
            pattern = en.ptrn_getvalue(ph, i, j)
            patterns.append(pattern)
        patterns_dict[id_] = patterns
    return patterns_dict
