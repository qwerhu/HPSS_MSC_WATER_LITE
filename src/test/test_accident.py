import unittest
from hyd.analysis import accident_analysis as acc

class TestAccident(unittest.TestCase):
  def test_quality(self):
    acc.get_qual_users('admin', 'inp')


if __name__ == "__main__":
    unittest.main()