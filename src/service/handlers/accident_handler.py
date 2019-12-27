import json
from service.handlers.base import BaseHandler
from hyd.analysis.accident_analysis import leak_analysis, valve_analysis, water_quality_analysis, get_quality_result, \
    get_leak_value_res
from utils import api_util


class LeakHandler(BaseHandler):
    async def get(self):
        """
        爆管分析
        :return:
        """
        points = self.get_argument('points', None)
        username = self.get_argument('username', None)
        type_ = self.get_argument('type', None)
        result = await api_util.call_blocking(leak_analysis, points, username, type_)
        self.write(json.dumps(result, ensure_ascii=False))


class ValveHandler(BaseHandler):
    async def get(self):
        """
        关阀分析
        :return:
        """
        ids = self.get_argument('ids', None)
        username = self.get_argument('username', None)
        type_ = self.get_argument('type', None)
        result = await api_util.call_blocking(valve_analysis, ids, username, type_)
        self.write(json.dumps(result, ensure_ascii=False))


class QualityHandler(BaseHandler):
    async def get(self):
        """
        水质分析
        :return:
        """
        points = self.get_argument('points', None)
        username = self.get_argument('username', None)
        result = await api_util.call_blocking(water_quality_analysis, points, username)
        self.write(json.dumps(result, ensure_ascii=False))


class QualResHandler(BaseHandler):
    async def get(self):
        """
        读取特定时间的水质事故结果
        :return:
        """
        username = self.get_argument('username', None)
        minute = self.get_argument('minute', None)
        result = await api_util.call_blocking(get_quality_result, username, minute)
        self.write(json.dumps(result, ensure_ascii=False))


class LeakValveResHandler(BaseHandler):
    async def get(self):
        """
        爆管关阀结果读取
        :return:
        """
        plan_id = self.get_argument('plan_id', None)
        type_ = self.get_argument('type', None)
        result = await api_util.call_blocking(get_leak_value_res, plan_id, type_)
        self.write(json.dumps(result, ensure_ascii=False))
