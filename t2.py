from test2 import collection_simulation


simulation_data_3 = collection_simulation.find({'SCADATYPE':3},{'_id':0}).limit(10)
simulation_data_2 = collection_simulation.find({'SCADATYPE':2},{'_id':0}).limit(10)
simulation_data_1 = collection_simulation.find({'SCADATYPE':1},{'_id':0}).limit(10)
simulation_data_0 = collection_simulation.find({'SCADATYPE':0},{'_id':0}).limit(10)


j = 0
for i in simulation_data_0:
    j = j + 1
    print('这是%d条数据，如下：'%(j))
    print(i)








