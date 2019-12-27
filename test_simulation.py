import time
import sys
from data import mod_simulation,historycl
from datetime import datetime,timedelta
from utils.dma_util import zbid2sid,sid2zbid
from service.handlers.base import BaseHandler


def get_simulation_before(stime,etime,target_id,data_type):

    result = mod_simulation.items(s=stime, e=etime,ids=[target_id],data_type=data_type)
    data_type_1 =result[0]['DATA']['type']
    print('你正在查询的过去的数据为%s数据' % (data_type_1))
    try:
        for i in result[0:1]:
            time_result = i.get('TIME')
            new_time = time.strftime('%Y-%m-%d %H:%M:%S',time_result)
            data_time = datetime.strptime(new_time,'%Y-%m-%d %H:%M:%S')
            i['TIME']= new_time
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
    except:
        print('数据为空、其他错误或者此时间段中无想要的数据')
    return befor


def get_simulation_after(stime,etime,target_id,data_type):
    result = mod_simulation.items(s=stime, e=etime, ids=[target_id], data_type=data_type)
    # print('未来的数据有%d个记录'%(len(result)))

    """
    下面的for循环中的每条数据就是隔了15分钟，即时间不同，其余的参数是相同的数据，取一条数据即可，上面的历史数据一样。
    """

    # for i in result:
    #     print(result)

    if not result:
        print('不存在这样的数据！！！！')
        sys.exit()

    try:
        for i in result[0:1]:
            # print('数据为：',i)
            time_result = i.get('TIME')
            new_time = time.strftime('%Y-%m-%d %H:%M:%S', time_result)
            data_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
            # print(time_result)
            # print(new_time)
            # print(data_time)
            i['TIME'] = new_time
            X = i.get('DATA')

            try:
                list_X = X['data']
                tagname = X['tagname']
                print('你的scada编号为：%s'% (tagname))
                data_type_1 = X['type']
                print('你正在查询的未来的数据为%s数据' % (data_type_1))
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
        return after,tagname
    except:
        print('有异常！！！')


def get_scada_data(stime,etime,id):
    stime1 = stime.timestamp()
    etime1 = etime.timestamp()
    history_data = historycl.items(s=stime1,e=etime1,Ids=[id])
    # scada_data = collection_scada.find({'endtime':1556087400,'starttime':1556001000},{'_id':0}).limit(10)
    # # scada_data = collection_scada.find({},{'_id':0}).limit(10)
    # list_cache = []
    # print(stime)
    # print(etime)
    # for i in scada_data:
    #     value = i.get('starttime')>=stime and i.get('endtime')<=etime
    #     print(i)
    # #     if id == id and value:
    # #         list_cache.append(i)
    # #     else:
    # #         pass
    # # print(list_cache)
    list_data = []
    list_data_jia = []
    interval = timedelta(minutes=15)
    for b in [history_data[i:i + 15] for i in range(0, len(history_data), 15)]:
        etime = etime -interval
        lol = {}
        x=0
        for i in b:
            x = x +i.get('value')
        lol['time'] = etime.strftime('%Y-%m-%d %H:%M:%S')
        lol['value'] = x
        list_data.append(lol)
    list_data = list_data[::-1]

    for i in history_data:
        list_data_jia.append(i.get('value'))
        # i['time'] = datetime.fromtimestamp(i.get('time')).strftime('%Y-%m-%d %H:%M:%S')
        # print(i)

    total_value = sum(list_data_jia)
    # print(total_value)
    return list_data


if __name__ == '__main__':
    pass
    # print('======' * 100)
    # interval = timedelta(hours=24)
    # # stime = '2019-04-23 14:30:00'
    # # etime = '2019-04-24 14:30:00'
    # # stime = '2019-12-19 00:00:00'
    # # etime = '2019-12-20 00:00:00'
    # # stime = '2019-12-19 07:00:00'
    # # etime = '2019-12-20 07:00:00'
    # stime = '2019-12-19 00:00:00'
    # etime = '2019-12-20 00:00:00'
    # stime_str = datetime.strptime(stime,'%Y-%m-%d %H:%M:%S')
    # etime_str = datetime.strptime(etime,'%Y-%m-%d %H:%M:%S')
    # etime_str1 = etime_str + interval
    # print('过去的开始时间',stime_str)
    # print('未来的开始时间和过去结束的时间',etime_str)
    # print('未来的结束时间',etime_str1)
    #
    # print('======' * 100)
    # target_id = 'WTP3-T2'
    # # target_id = 'P-14004'
    # # target_id = 'P-0198'
    # data_type = 0
    #
    # final_result = {}
    # final_result_total = {}
    # befor_result = get_simulation_before(stime=stime_str,etime=etime_str,target_id=target_id,data_type=data_type)
    # print('before have %d group' %(len(befor_result)))
    # # print(befor_result)
    # final_result['before'] = befor_result[::-1]
    #
    #
    # after_result,tagname = get_simulation_after(stime=etime_str,etime=etime_str1,data_type=1,target_id=target_id)
    # print('after have %d group' % (len(after_result)))
    # final_result['after'] = after_result
    #
    #
    # id = zbid2sid(tagname) #t_scada_cleaning中的id
    # print('t_scada_cleaning中的id为%s'%(id))
    # scada_data =get_scada_data(stime=stime_str,etime=etime_str,id=id)
    # print('scada have %d group' % (len(scada_data)))
    # final_result['scada'] = scada_data
    #
    # print('======'*100)
    # print('未来、过去和scada数据结果的集合(1)', final_result)
    #
    #
    # # print('======' * 100)
    # # print('过去24小时的----%s----历史数据，按每15分钟一次，加在后面的时间点上(最开始去第一个)：'%(data_type1))
    # print(final_result['before'])
    # # print('未来24小时的-----%s-----历史数据，按每15分钟一次，加在后面的时间点上（最开始取第一个）：'%(data_type1))
    # print(final_result['after'])
    # # print('过去24小时的scada的---%s----历史数据，按每15分钟一次，加在后面的时间点上(最开始取第一个)：'%(data_type1))
    # print(final_result['scada'])
    #
    # #尝试将ME10004411_2转化为scanda数据的id(即H_ME10004411_2_HBJTYWTYJL)
    # x = zbid2sid('ME10006922_2')
    # y = zbid2sid('ME10004411_2')
    # print(x,y)
