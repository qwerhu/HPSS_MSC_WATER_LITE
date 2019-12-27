import unittest
import time
from hyd.analysis.model_result import ModelResult
from hyd.analysis import model_function
from hyd.analysis import get_modelobj_info
from hyd.realtime import enums


class ModelResultTest(unittest.TestCase):
    """
    ModelResult 测试
    """
    def test_get_one(self):
        t = time.time()
        m = ModelResult('online_after')
        d = m.get_node_data('J-100678')
        print('test get one cost {}'.format(time.time() - t))
        self.assertNotEqual(d, None, 'get one node')
        t = time.time()
        d1 = m.get_node_data('J-100678', period=1)
        print('test get one with period cost {}'.format(time.time() - t))

        t = time.time()
        d2 = m.get_node_data_test('J-100678')
        print('test new cost {}'.format(time.time() - t))
        t = time.time()
        d1 = m.get_node_data_test('J-100678', period=1)
        print('test get new one with period cost {}'.format(time.time() - t))

        self.assertNotEqual(d1, None, 'get one node with period')

    def test_get_all_node(self):
        t = time.time()
        m = ModelResult('online_after')
        d = m.get_all_node_data()
        # print(d)
        print('test get all node cost {}'.format(time.time() - t))
        self.assertNotEqual(d, None, 'get all node')
        t = time.time()
        d1 = m.get_all_node_data(10)
        print('test get all node with period cost {}'.format(time.time() - t))
        t = time.time()
        d2 = m.get_node_data_test()
        print('new: test get all node cost {}'.format(time.time() - t))
        t = time.time()
        d2 = m.get_node_data_test(period=10)
        print('test get all node with period cost {}'.format(time.time() - t))

        self.assertNotEqual(d1, None, 'get all node with period')

    def test_get_one_link(self):
        t = time.time()
        m = ModelResult('online_before')
        d = m.get_link_data('P-13610')
        print('test get one link cost {}'.format(time.time() - t))
        self.assertNotEqual(d, None, 'get one link')
        t = time.time()
        d1 = m.get_link_data('P-13610', period=1)
        print('test get one link with period cost {}'.format(time.time() - t))
        self.assertNotEqual(d1, None, 'get one link with period')

    def test_get_all_link(self):
        t = time.time()
        m = ModelResult('online_before')
        d = m.get_all_link_data()
        # print(d)
        print('test get all link cost {}'.format(time.time() - t))
        self.assertNotEqual(d, None, 'get all link')
        t = time.time()
        d1 = m.get_all_link_data(10)
        print('test get all link with period cost {}'.format(time.time() - t))
        self.assertNotEqual(d1, None, 'get all link with period')

    def test_get_model_info(self):
        m = ModelResult('online_before')
        m.get_model_info()

    def test_get_pump(self):
        res = ModelResult('online_before').get_all_pump_data(10, is_dict=True)
        self.assertNotEqual(res, None)


class ModelFuncTest(unittest.TestCase):
    def test_get_model_res(self):
        res = model_function.get_model_hyd_res('online_before', enums.ModelResultType.Node, 'WTP3-T1')
        print(res)

    def test_get_model_param(self):
        res = model_function.get_model_paras('online_after', 'J-74950', '1')
        print(res)

    def test_get_model_para(self):
        res = get_modelobj_info.get_model_para('online_after', 'J-73258', enums.ModelObjectType.Meter)
        print(res)


if __name__ == '__main__':
    unittest.main()
