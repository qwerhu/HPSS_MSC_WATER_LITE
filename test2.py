from pymongo import MongoClient

# client = MongoClient('localhost',27017)
#
# print('select database')
# # db = client.hunan
# db=client['hunan']
# print(db)
# print('show all databases')
# dbs = client.list_database_names()
# print(dbs)
# print('show all collections of current database ')
# db_collections111 = db.list_collection_names()
# print(db_collections111)
# print('Have %d collections'% len(db_collections111))
# print('=='*8)
# db_collection = db['changsha']
# print(db_collection)
# print('=='*8)
# for i in db_collection.find({}):
#     print(i)
# print(db_collection.find_one())
# result_value = db_collection.insert_many([{'_id':3,'place':'怀化','number':89},{'_id':4,'place':'罗旧','number':88}])
# print(result_value)

client = MongoClient('10.10.1.127',27017)

#show all databases
dbs = client.list_database_names()

# print(dbs)
#connect the database

db=client['modeldb']
# print(db)
db1 = client['scadadb_history']



#show all document
collections = db.list_collection_names()

collection_simulation = db['model_result_simulation']
collection_volume = db['model_result_volume']
collection_scada = db1['t_scada_cleaning']
print(collection_scada)


# print(collection_simulation)
# print(collection_volume)
# print('**'*40)

# list_targetid = []
# for value in collection_volume.find({}).limit(10):
#     # print(value)
#     TARGET_ID_value =value.get('TARGET_ID')
#     if TARGET_ID_value in list_targetid:
#         print("%s is cached"% (TARGET_ID_value))
#     else:
#         list_targetid.append(TARGET_ID_value)
    # list.append(value.get('TARGET_ID'))
    # print(type(value))
# print(list_targetid,len(list_targetid))

# #transfer the str to datatime
# value_1 = list[0].get('DATA_DATE')
# print(value_1,type(value_1))






