from  datetime import datetime,timedelta
from  data import mod_volume,mod_simulation
from test2 import collection_volume,collection_simulation,client

# current_time = datetime.now()
# before_current_time = current_time - timedelta(hours=24)
# future_current_time = current_time+timedelta(hours=24)
# current_time1 = current_time.strftime('%Y-%m-%d %H:%M:%S')
# before_current_time1 = before_current_time.strftime('%Y-%m-%d %H:%M:%S')
# print('current time:%s '% (current_time1))
# print('before_current_time:%s'% (before_current_time1))
# # # print(current_time)
# #
# # current_time1 = datetime.strptime('2019-04-24 00:00:00','%Y-%m-%d %H:%M:%S')
# # print('ok')
# # current_time_stamp = current_time.timestamp()
#
# before_current_time_stamp = before_current_time.timestamp()
# print(current_time_stamp)
# print(before_current_time_stamp)
#
# # r = mod_volume.items(s=before_current_time,e=current_time,data_type=0)
# # print(r)
# # print(r[58])
# # print(len(r))
# forcast_data= mod_simulation.items(s=before_current_time,e=current_time,ids=['P-0158'] , data_type=0)
# # future_data= mod_simulation.items(s=before_current_time,e=current_time,ids=['P-0158'] , data_type=0)
# # before_data = mod_simulation.items(e=future_current_time,s=current_time1,ids=['J-106830'] ,data_type=1)
# # print(len(before_data))
# # print(before_data[0])
# # print(before_data[1])
# # print(before_data[2])
# # print(len(future_data))
# # print(future_data[0])
# # print(future_data[1])
# # print(future_data[2])
# # print(forcast_data)
# print(len(forcast_data))
# print(forcast_data[1])
# print(forcast_data[2])


x = datetime.fromtimestamp(1554784560)
print(x)

