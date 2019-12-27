import time
import unittest
from hyd.analysis import model_function, best_path


class TestBestPath(unittest.TestCase):
    def test_best_path(self):
        t = time.time()
        elements = model_function.get_model_nodes('online_before')
        res = best_path.get_path_weight('J-78206', 'J-78189', elements)
        print('test best path cost: {}'.format(time.time() - t))
        self.assertNotEqual(res, None)


if __name__ == '__main__':
    unittest.main()
