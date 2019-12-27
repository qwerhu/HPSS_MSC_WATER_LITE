import json
import unittest
from hyd.analysis import out2json
from hyd.realtime import enums


class TestOutToJson(unittest.TestCase):

    def test_out_json(self):
        o = out2json.OutToJson('online_before_q_4490', analysis_type=enums.AnalysisType.Quality)
        o.run()
        # o = out2json.OutToJson('online_before_4490')
        # o.run()
        # n = out2json.OutToJson('online_after_4490')
        # n.run()

    # p = r"G:\HugeGIS_WS\HPSS\HPSS_MSC_WATER\assert\online_before"
    # c = 0
    # for i in range(49):
    #     temp_p = '{}\\{}\\node.json'.format(p, str(i))
    #     try:
    #         with open(temp_p) as f:
    #             json.load(f)
    #         c += 1
    #     except Exception as err:
    #         print('{}: {}'.format(i, err))


