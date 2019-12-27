import unittest
from hyd.edit.setter_time import SetterTime
from hyd import edit

class TestEdit(unittest.TestCase):

    def test_time(self):
        l = []
        t = SetterTime(duration=86400, hydstep=3600, qualstep=3600, starttime=43200, patternstep=3600, reportstep=3600)
        l.append(t)
        l.append(SetterTime(patternstep=300))
        edit.save(l, 'net_test')
        # t.save_file('../assert/net_test.inp')
