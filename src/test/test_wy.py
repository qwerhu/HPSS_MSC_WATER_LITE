import time
import unittest
from datetime import datetime
from hyd.analysis.out2dict import OutToDict
from hyd.report.report_vol import ReportVol
from hyd.realtime import enums, real_deamnd, real_pump, real_rawwater, real_tank, real_timeparam
from utils import model_util
from hyd.realtime.enums import FlowType, VolumeType, OnlineType
from hyd.realtime.demand import base_demand, demand_pattern


class TestSimulation(unittest.TestCase):
    def test_sim1(self):
        id_list = ['WTP2-T2', 'SWWTP-T1', 'SWWTP-T2', 'WTP3-T1', 'WTP3-T2', 'WTP1-T1', 'WTP1-T2', 'WTP2-T1']
        time_idx = 288
        t = time.time()
        df_nodes = OutToDict('online_before').get_data()['df_nodes']
        print('get data cost time: %f' % (time.time() - t))
        t = time.time()
        tank_data = df_nodes.loc[(df_nodes['id'].apply(lambda x: x in id_list)) & (df_nodes['period'] == time_idx)]
        print('get data cost time: %f' % (time.time() - t))
        for model_id in id_list:
            tanklevel = tank_data.loc[tank_data['id'] == model_id]['PRESSURE'][0]

    def test_wy(self):
        target_date = datetime.strptime('2019-05-17 10:00:00', '%Y-%m-%d %H:%M:%S')
        target_timestamp = model_util.align_online_time(target_date)
        s = target_timestamp - 86400
        e = target_timestamp
        cus_tags = ["meter_flow_321"]
        cus_scada_data = model_util.get_scada_data(cus_tags, s, e)
        dmd_cus = base_demand.RelDemand(cus_scada_data, target_date, "meter_flow_321", VolumeType.VipCustomer.value)
        dmd_cus_value = dmd_cus.run(online_type=enums.OnlineType.HUISUAN, is_save=False)
        ptn_cus = demand_pattern.RelPattern(cus_scada_data, target_date, "meter_flow_321", VolumeType.VipCustomer.value)
        ptn_cus_value = ptn_cus.run(online_type=enums.OnlineType.HUISUAN, is_save=False, base_demand=dmd_cus_value)
