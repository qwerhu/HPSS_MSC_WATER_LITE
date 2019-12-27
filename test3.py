import time
from datetime import datetime,timedelta
from test2 import client,collection_volume,collection_simulation
from data import mod_volume


#acquire simulation data
def get_result_simulation_data(target_id):
    target_id_object =collection_simulation.find({},{'TARGET_ID':1}).limit(50)
    list_target_id = []

    for i in target_id_object:
        target_id_value = i.get('TARGET_ID')
        list_target_id.append(target_id_value)
    # print(list_target_id)

    if target_id in list_target_id:
        j = 0
        for i in collection_simulation.find({'TARGET_ID': target_id}, {'_id': 0}).limit(5):
            time.sleep(2)
            j += 1
            print('%d data: %s' % (j, str(i)))
    else:
        print("can't None and value don't exists")


#acquire volume data
def get_result_volume_data(target_id):
    target_id_object = collection_volume.find({}, {'TARGET_ID': 1}).limit(50)
    list_target_id = []

    for i in target_id_object:
        target_id_value = i.get('TARGET_ID')
        list_target_id.append(target_id_value)
    # print(list_target_id)

    if target_id in list_target_id:
        j = 0
        for i in collection_volume.find({'TARGET_ID':target_id},{'_id':0}).limit(5):
            time.sleep(1)
            j +=1
            print('%d data: %s'%(j,str(i)))
    else:
        print("can't None and value don't exists")


def get_result_simulation_data1(target_id):
    pass


def get_result_volume_data1(target_id):
    target_id_object = collection_volume.find({}, {'TARGET_ID': 1}).limit(50)
    list_target_id = []
    for i in target_id_object:
        target_id_value = i.get('TARGET_ID')
        list_target_id.append(target_id_value)


    current_time = datetime.now()
    time_delt = timedelta(hours=24)
    before_time = current_time - time_delt
    if target_id in list_target_id:
        j = 0
        for i in collection_volume.find({'TARGET_ID': target_id}, {'_id': 0}).limit(5):
            time.sleep(1)
            j += 1
            print('%d data: %s' % (j, str(i)))
    else:
        print("can't None and value don't exists")


if __name__ == '__main__':
    # list_targetid = []
    # for value in collection_volume.find({}).limit(10):
    #     TARGET_ID_value = value.get('TARGET_ID')
    #     if TARGET_ID_value in list_targetid:
    #         # print("%s is cached" % (TARGET_ID_value))
    #         pass
    #     else:
    #         list_targetid.append(TARGET_ID_value)
    # print('please you input one of these test data %s '%(str(list_targetid)))
    # # targetid_1 = str(input("input you targetid:"))
    # print("=====" * 10+ 'volume'+ "=====" * 10)
    # get_result_volume_data(target_id='alldemand')
    # print("=====" * 10+ 'simulation'+ "=====" * 10)
    # get_result_simulation_data(target_id='P-0158')
    result_data = {}
    get_result_volume_data1(target_id=None)


