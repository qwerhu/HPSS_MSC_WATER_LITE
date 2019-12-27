from tornado.web import Application
from service.handlers import  schedule_handler
import handler_simulation


class WsApplication(Application):
    def __init__(self):
        handlers = [
            (r'/api/schedule', schedule_handler.SchHadl),
            (r'/api/test',handler_simulation.HuHandler)
            # 手动执行指定时间的在线模型分析
            # (r'/api/online/manual', model_handler.OnlineSimulationHdl),
            # # 模型计算结果数据
            # (r'/api/model/result/simulation', rs_handler.RSHandler),
            # # 模型计算过程数据
            # (r'/api/model/result/volume', rv_handler.RVHander),
            # # 历史数据查询接口（原始）
            # (r'/api/scada/his', scada_handler.ScadaHisRawHandler),
            # # 历史数据查询接口（已清洗）
            # (r'/api/scada/his/cleaning', scada_handler.ScadaHisCLHandler),
            # # 压力报表
            # (r'/api/model/report/press', rpt_handler.PressHandler),
            # # 详细报表
            # (r'/api/model/report/detail', rpt_handler.DetailHandler),
            # # 爆管分析
            # (r'/api/model/accident/leak', accident_handler.LeakHandler),
            # # 关阀分析
            # (r'/api/model/accident/valve', accident_handler.ValveHandler),
            # # 水质分析
            # (r'/api/model/accident/quality', accident_handler.QualityHandler),
            # # 特定时间点的水质分析结果
            # (r'/api/model/accident/quality_res', accident_handler.QualResHandler),
            # # 爆管或关阀结果
            # (r'/api/model/accident/leak_valve_res', accident_handler.LeakValveResHandler),
            # # 离线方案
            # (r'/api/model/plan/save', model_plan_handler.SavePlanHandler),
            # (r'/api/model/plan/change', model_plan_handler.ChangePlanHandler),
            # (r'/api/model/plan/delete', model_plan_handler.DelPlanHandler),
            # # 泵站调度
            # (r'/api/model/schedule/pump_info', pump_ctrl_handler.PumpInfoHandler),
            # (r'/api/model/schedule/pump_head', pump_ctrl_handler.PumpHByQHandler),
            # (r'/api/model/schedule/pump_status', pump_ctrl_handler.PumpStatusHandler),
            # (r'/api/model/schedule/modify_simulation', pump_ctrl_handler.HydSimHandler),
            # (r'/api/model/schedule/pump_res', pump_ctrl_handler.PumpResHandler),
            # (r'/api/model/schedule/station_tree', pump_ctrl_handler.StationTreeHandler),
            # # GIS数据同步
            # (r'/api/model/sync/update', model_sync_handler.ModelSyncHandler),
            # # 模型规划
            # (r'/api/model/modify', model_modify_handler.ModelModifyHandler),
            # # 模型路径分析
            # (r'/api/model/path', best_path_handler.ProfileDataHandler),
            # # 模型静态参数(单个ID)
            # (r'/api/model/info', model_func_handler.ModelInfoHandler),
            # # 获取管线的报警信息以及上次回算的最后一个时刻的压降数据
            # (r'/api/model/water_path', model_func_handler.WaterPathHandler),
            # # 获取报警的SCADA
            # (r'/api/model/press_alarm', model_func_handler.PressAlarmHandler),
            # # 模型分析节点全部结果
            # (r'/api/model/node_res', model_func_handler.NodeResHandler),
            # # 模型静态参数(多个ID）
            # (r'/api/model/paras', model_func_handler.ModelParasHandler),
            # # 查询调度方案的配水电单耗数据
            # (r'/api/model/schedule/station_energy', model_func_handler.StationEnengyHandler),
            # # 删除方案分组
            # (r'/api/model/plan/del_program_group', model_func_handler.DelProgGroupHandler),
            # # 查询方案修改的模型构建数据
            # (r'/api/model/plan/model_relation_change', model_func_handler.ModelRelationHandler),
            # # 查询用户客户、管线、阀门口径大小的列表
            # (r'/api/model/diameters', model_func_handler.DiametersHandler),
            # # 模型结果缓存更新接口
            # (r'/api/model/cache/update', model_func_handler.UpdateCacheHandler)
        ]
        super().__init__(handlers)
