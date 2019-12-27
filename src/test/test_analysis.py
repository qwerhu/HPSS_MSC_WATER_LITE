import time
import traceback
import unittest
import asyncio
from hyd.analysis.out2shp import OutToShape
from hyd.analysis.out2json import OutToJson


class TestAnalysis(unittest.TestCase):

    def test_shp(self):
        t = time.time()
        try:
            s = OutToShape('online_before')
            # s = OutToShape('net')
            s.run()
        except Exception as e:
            traceback.print_exc()
        print(f'time used {time.time()-t}')

    def test_json(self):
        t = time.time()
        try:
            s = OutToJson('online_before')
            s.run()
        except Exception:
            traceback.print_exc()
        print(f'time used {time.time() - t}')
