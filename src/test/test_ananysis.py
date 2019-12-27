from hyd.analysis import accident_analysis
from hyd.edit import save
import unittest
from datetime import datetime


class TestAccident(unittest.TestCase):
    def test_mup_time(self):
        dt = datetime(2019,8,11,10,20,0,0)
        muptime = accident_analysis.get_muptime(dt)
        print(muptime)

    def test_leak_part_als(self):
        s_list = []
        # 设置最不利点的patern，valve，tank，rule等
        model_setter = accident_analysis.get_mup_modelsetter(10, None, 'admin')
        s_list.extend(model_setter)
        save(s_list, 'admin')


if __name__ == '__main__':
    unittest.main()