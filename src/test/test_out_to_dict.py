import time
import unittest
from hyd.analysis import out2dict


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


class TestOutRead(unittest.TestCase):
    def test_out_read(self):
        o = out2dict.OutToDict('online_after')
        t = time.time()
        data = o.get_data()
        print('first out cost: {}'.format(time.time() - t))
        t = time.time()
        data2 = o.get_data()
        print('second out cost: {}'.format(time.time() - t))
        # self.assertEqual(len(data), len(data2))


if __name__ == '__main__':
    unittest.main()
