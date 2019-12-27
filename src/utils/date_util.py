import time
import copy
import os
from enum import Enum
from datetime import datetime, timedelta
import ctx

FORMAT_DATE = '%Y-%m-%d'


def get_timestamp():
    """
    返回毫秒级时间戳
    :return:
    """
    return int(time.time() * 1000)


def get_dirname(root_path, n=1):
    """
    :param root_path: 给定的文件或目录
    :param n: 要获取父目录的层级
    :return: 指定层级的父目录
    """
    if n == 0:
        return root_path

    path_ = os.path.dirname(root_path)
    if n == 1:
        return path_
    else:
        return get_dirname(path_, n - 1)


def get_cost_time(cost, valid=2):
    """
    @note: 以分秒的格式计算运行时间
    """
    min_unit = ' m  '
    sec_unit = ' s  '
    if cost >= 60:
        minutes = str(int(cost // 60)) + min_unit
        seconds = str(int(cost % 60)) + sec_unit
    else:
        minutes = ''
        seconds = str(round(cost % 60, valid)) + sec_unit
    return minutes + seconds


def get_standard_date(dt):
    """
    :param dt: 原始datetime格式的时间
    :return: 0, 15, 30, 45.
    """
    t = dt.timestamp()
    t = t - t % ctx.online_compute_step
    res = datetime.fromtimestamp(t)
    # duration = int(ctx.online_compute_step / 60)
    # minute = dt.minute
    # # minute = '0'
    # minute = str(int(minute / duration * duration))
    # year = str(dt.year)
    # month = str(dt.month)
    # day = str(dt.day)
    # hour = str(dt.hour)
    # dt_str = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"
    # res = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return res


class DayType(Enum):
    Workday = 0
    Holiday = 1


class Holidays(object):

    def __init__(self):
        """
        初始化，获取节假日数据
        配置数据格式：
        {
        name:'节日名称',
        s_date: '开始日期，如2019-10-01',
        e_date: '结束日期',
        workdays:'调休日期,多个用逗号分隔'
        }
        """
        self.holidays = []
        self.workdays = []

    def is_holiday(self, str_date):
        """
        判断是否为假期
        :param str_date: 日期字符串，如2019-03-11
        :return: True or False
        """
        if isinstance(str_date, datetime):
            str_date = str_date.strftime(FORMAT_DATE)
        elif isinstance(str_date, time.struct_time):
            str_date = time.strftime(FORMAT_DATE, str_date)

        if str_date in self.holidays:
            return True
        if str_date in self.workdays:
            return False
        _date = datetime.strptime(str_date, '%Y-%m-%d')
        return _date.weekday() in [5, 6]

    def get_day_type(self, _date, date_format='%Y-%m-%d'):
        if isinstance(_date, str):
            _date = datetime.strptime(_date, date_format)
        elif isinstance(_date, time.struct_time):
            _date = datetime(*_date[:6])
        str_date = _date.strftime('%Y-%m-%d')
        return DayType.Holiday if self.is_holiday(str_date) else DayType.Workday

    def get_same_days(self, num_days, date_type=None, s_date=None):
        """
        获取相同类型的日期列表
        :param num_days: 要获取的日期数量
        :param date_type: 日期类型， DayType
        :param s_date: 开始日期（截止日期）
        :return:
        """
        if s_date is None:
            s_date = datetime.today()
        else:
            s_date = copy.deepcopy(s_date)
        if date_type is None:
            date_type = DayType.Workday
        date_list = []
        while len(date_list) < num_days:
            # 不包括截至日期
            s_date -= timedelta(days=1)
            if date_type == self.get_day_type(s_date):
                date_list.append(s_date)
        date_list.reverse()
        return date_list


HOLIDAYS = Holidays()
