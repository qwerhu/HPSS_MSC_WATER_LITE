from datetime import datetime
from pymongo import MongoClient

#远程数据库
client = MongoClient('10.10.1.127',27017)
db=client['modeldb']
db1 = client['scadadb_history']

#本地数据库
client1 = MongoClient('127.0.0.1',27017)
db2 = client1['history_data']

def insert_data_local(collection_name,data):
    collection_table = db2[collection_name]
    for i in data:
        x = collection_table.insert_one(i)
        print(x)


def read_data_remote(collection_name):
    gb = []
    collection_table = db1[collection_name]
    items = collection_table.find({},{'_id':0}).limit(1000)
    for i in items:
        # print(i)
        gb.append(i)
    return gb


if __name__ == '__main__':
    remote_data = read_data_remote('t_scada_his_3600')
    # print(remote_data[0])
    # print(len(remote_data))
    insert_data_local('t_scada_his_3600',data=remote_data)




