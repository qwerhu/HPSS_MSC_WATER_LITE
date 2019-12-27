import unittest
import json
from hyd.analysis import model_modify


class TestModelModify(unittest.TestCase):
  def test_model_modify(self):
    # data = {"Nodes":[{"x":"470910.91","y":"4379260.86","oldId":"J-72607","BASEDEMAND":0,"newId":"J25703"},{"x":"470905.34","y":"4379443.14","oldId":"","BASEDEMAND":0,"newId":"J24675"},{"x":"470980.75","y":"4379457.70","oldId":"","BASEDEMAND":0,"newId":"J49301"}],"Pipes":[{"DIAMETER":"100","ENDID":"J24675","ID":"P71447","MATERIAL":"球墨铸铁","STARTID":"J25703"},{"DIAMETER":"100","ENDID":"J49301","ID":"P88051","MATERIAL":"球墨铸铁","STARTID":"J24675"}],"UserName":"admin","PlanID":""}
    data = {"Nodes":[{"x":116.66772102,"y":39.55335426,"oldId":"J-77662","BASEDEMAND":0,"newId":"J53679"},{"x":116.66576785702374,"y":39.553209132010565,"oldId":"","BASEDEMAND":0,"newId":"J40836"},{"x":116.66562838215496,"y":39.55507594948493,"oldId":"","BASEDEMAND":0,"newId":"J48978"},{"x":116.66769904751446,"y":39.5553227127143,"oldId":"","BASEDEMAND":0,"newId":"J13379"}],"Pipes":[{"DIAMETER":"100","ENDID":"J40836","ID":"P73022","MATERIAL":"铸铁","STARTID":"J53679"},{"DIAMETER":"100","ENDID":"J48978","ID":"P78904","MATERIAL":"铸铁","STARTID":"J40836"},{"DIAMETER":"100","ENDID":"J13379","ID":"P46576","MATERIAL":"铸铁","STARTID":"J48978"}],"UserName":"testadmin","PlanID":""}
    data = json.dumps(data, ensure_ascii=False)
    model_modify.model_modify_deal(data)


if __name__ == "__main__":
    unittest.main()