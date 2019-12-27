import time
import traceback
import unittest
from hyd.analysis.save_result import SaveResult
from hyd.realtime import enums
from hyd.analysis.out2dict import OutToDict


class TestAnalysis(unittest.TestCase):

    def test_save(self):
        t = time.time()
        try:
            s = SaveResult('online_after', enums.OnlineType.YUCE)
            s.main()
        except Exception:
            traceback.print_exc()
        print(f'time used {time.time() - t}')

    def test_pump_freq(self):
        all_data = OutToDict('online_after').get_data()
        num_periods = all_data['num_periods']
        df_nodes = all_data['df_nodes']
        df_links = all_data['df_links']
        temp_df_link = df_links.loc[0]
        status = int(temp_df_link.loc[freq_key, constants.LINK_FIELD_STATUS])
        status = constants.OPEN if status == 1 else constants.CLOSED
        frequency = str(round(float(temp_df_link.loc[freq_key, constants.LINK_FREQUENCY]) * 50, 1))
        ptime = (self.dt + timedelta(minutes=5 * peri)).strftime(constants.FORMAT_DATA_DATE)
