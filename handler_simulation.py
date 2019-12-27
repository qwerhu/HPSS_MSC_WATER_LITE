import time
import json
from datetime import datetime,timedelta
from service.handlers.base import BaseHandler
from utils.dma_util import zbid2sid
from data import mod_simulation,historycl


class HuHandler(BaseHandler):
    async def get(self):
        # 获取编号
        interval = timedelta(hours=24)
        target_id = self.get_argument('target_id', None)
        data_type = int(self.get_argument('data_type', 0))
        tagname = self.get_argument('scadaid',None)
        id = zbid2sid(tagname)
        if not target_id:
            self.return_failed()
            return
        etime = self.get_argument('etime', '2019-12-20 00:00:00')
        etime_str = datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        stime_str = etime_str - interval
        etime_str1 = etime_str + interval
        print('过去的开始时间', stime_str)
        print('未来的开始时间和过去结束的时间', etime_str)
        print('未来的结束时间', etime_str1)
        final_result = {}


        #获取过去24小时的数据
        def get_simulation_before(stime, etime, target_id, data_type):
            result = mod_simulation.items(s=stime, e=etime, ids=[target_id], data_type=data_type)
            try:
                for i in result[0:1]:
                    time_result = i.get('TIME')
                    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time_result)
                    data_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
                    i['TIME'] = new_time
                    X = i.get('DATA')
                    try:
                        list_X = X['data']
                    except:
                        print('no the value')

                    time_delt = timedelta(minutes=15)
                    befor = []

                    for b in [list_X[i:i + 3] for i in range(0, len(list_X), 3)]:
                        lol = {}
                        x = 0
                        for i in b:
                            x = x + i
                        lol['time'] = data_time.strftime('%Y-%m-%d %H:%M:%S')
                        lol['value'] = x
                        data_time = data_time - time_delt
                        befor.append(lol)
                    return befor
            except:
                print('数据为空、其他错误或者此时间段中无想要的数据')


        #获取未来24小时的数据
        def get_simulation_after(stime, etime, target_id, data_type):
            result = mod_simulation.items(s=stime, e=etime, ids=[target_id], data_type=data_type)
            try:
                for i in result[0:1]:
                    time_result = i.get('TIME')
                    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time_result)
                    data_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
                    i['TIME'] = new_time
                    X = i.get('DATA')
                    try:
                        list_X = X['data']
                    except:
                        print('no the value')

                    time_delt = timedelta(minutes=15)
                    after = []
                    for b in [list_X[i:i + 3] for i in range(0, len(list_X), 3)]:
                        lol = {}
                        data_time = data_time + time_delt
                        x = 0
                        for i in b:
                            x = x + i
                        lol['time'] = data_time.strftime('%Y-%m-%d %H:%M:%S')
                        lol['value'] = x
                        after.append(lol)
                    return after
            except:
                after = []
                print('有异常！！！')

        #取出scada数据
        def get_scada_data(stime, etime, id):
            stime1 = stime.timestamp()
            etime1 = etime.timestamp()
            history_data = historycl.items(s=stime1, e=etime1, Ids=[id])
            list_data = []
            interval = timedelta(minutes=15)
            for b in [history_data[i:i + 15] for i in range(0, len(history_data), 15)]:
                lol = {}
                x = 0
                for i in b:
                    x = x + i.get('value')
                etime = etime - interval
                lol['time'] = etime.strftime('%Y-%m-%d %H:%M:%S')
                lol['value'] = x
                list_data.append(lol)
            list_data = list_data[::-1]
            return list_data

        try:
            if data_type == 0:
                befor_result = get_simulation_before(stime=stime_str, etime=etime_str, target_id=target_id,
                                                 data_type=0)
                final_result['before'] = befor_result[::-1]
            elif data_type == 1:
                after_result= get_simulation_after(stime=etime_str, etime=etime_str1,
                                                                             data_type=1, target_id=target_id)
                final_result['after'] = after_result
            else:
                pass
            scada_data = get_scada_data(stime=stime_str, etime=etime_str, id=id)
            final_result['scada'] = scada_data
            self.write(json.dumps(final_result, ensure_ascii=False))
        except:
            pass







