import time
import unittest
from os import path
from hyd.simulation.simulation import Simulation
from hyd.simulation import hyd_simulation
from hyd.analysis import model_function
from hyd.realtime.enums import ModelTemplateType


class TestSimulation(unittest.TestCase):

    def test_sim(self):
        t = time.time()
        s = Simulation('online_after_4490')
        # s = Simulation('net_test')
        # s = Simulation('online')
        out, annex = s.run(False)
        print(f'time used {time.time() - t}')
        self.assertEqual(path.exists(out), True, 'out')
        self.assertEqual(path.exists(annex), True, 'annex')
        # before
        s = Simulation('online_before_4490')
        out, annex = s.run(False)
        self.assertEqual(path.exists(out), True, 'out')
        self.assertEqual(path.exists(annex), True, 'annex')

    def test_sim_q(self):
        model_function.set_model_type("online_before_q_4490", ModelTemplateType.WaterAge)
        Simulation('online_before_q_4490').run(True)



