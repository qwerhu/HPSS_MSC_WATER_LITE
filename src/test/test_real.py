import unittest
from datetime import datetime
from hyd.realtime import real_tank
from hyd.realtime import enums


class TestReal(unittest.TestCase):
    def test_real_tank(self):
        temp_date = datetime(2019,8,11,11,0,0)
        setters = real_tank.run(temp_date, enums.OnlineType.YUCE)
        self.assertNotEqual(setters, None)
        self.assertNotEqual(len(setters), 0)


if __name__ == '__main__':
    unittest.main()
