from datetime import datetime
import unittest
from hyd.simulation import quality_simulation
from hyd.realtime import enums


class MyTestCase(unittest.TestCase):
    def test_simulation(self):
        dt = datetime.now()
        quality_simulation.run_quality_simulation(dt, enums.OnlineType.HUISUAN)


if __name__ == '__main__':
    unittest.main()
