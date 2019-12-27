"""
常量
"""
# from epanet.output import output as oapi
# from epanet.toolkit import toolkit as en

# out文件读取
NODE_FIELD_ID = 'ID'
NODE_FIELD_PRESSURE = 'PRESSURE'
NODE_FIELD_HEAD = 'HEAD'
NODE_FIELD_QUALITY = 'QUALITY'
NODE_FIELD_DEMAND = 'DEMAND'
LINK_FIELD_ID = 'ID'
LINK_FIELD_STATUS = 'STATUS'
LINK_FIELD_FLOW = 'FLOW'
LINK_FIELD_VELOCITY = 'VELOCITY'
LINK_FIELD_HEADLOSS = 'HEADLOSS'
LINK_FIELD_QUALITY = 'QUALITY'
LINK_FIELD_PRESSDROP = 'PRESSDROP'
LINK_FIELD_ENERGY = 'ENERGY'
LINK_FIELD_DIRECTION = 'DIRECTION'

LINK_FREQUENCY = 'SETTING'  # dengyu add
PRESS = 0
FLOW = 1
WATER_LEVEL = 2
WATER_USAGE = 3
WATER_REPORT = 4
PUMP_OPERATION = 5
PUMP_ENERGY = 6
PUMP_FREQUENCY = 7
PRESS_AREA = 8
DETAIL_REPORT = 9
STATION_ENERGY = 10

FORMAT_DATA_DATE = '%Y-%m-%d %H:%M:%S'
OPEN = 'OPEN'
CLOSED = 'CLOSED'  # dengyu add

NODE_PRESSURE = oapi.NodeAttribute.PRESSURE
NODE_DEMAND = oapi.NodeAttribute.DEMAND
NODE_HEAD = oapi.NodeAttribute.HEAD
NODE_QUALITY = oapi.NodeAttribute.QUALITY
LINK_FLOW = oapi.LinkAttribute.FLOW
LINK_VELOCITY = oapi.LinkAttribute.VELOCITY
LINK_HEADLOSS = oapi.LinkAttribute.HEADLOSS
LINK_AVG_QUALITY = oapi.LinkAttribute.AVG_QUALITY
LINK_STATUS = oapi.LinkAttribute.STATUS
LINK_SETTING = oapi.LinkAttribute.SETTING
LINK_DIRECTION = 'direction'
LINK_ENERGY = 'energy'

N_COLUMNS = [NODE_PRESSURE, NODE_DEMAND, NODE_HEAD, NODE_QUALITY]
L_COLUMNS = [LINK_FLOW, LINK_VELOCITY, LINK_HEADLOSS, LINK_AVG_QUALITY, LINK_STATUS, LINK_SETTING]

# simulation
PIPE_TYPES = [en.LinkType.CVPIPE.value, en.LinkType.PIPE.value]
VALVE_TYPES = [en.LinkType.FCV.value, en.LinkType.GPV.value, en.LinkType.PBV.value, en.LinkType.PRV.value,
               en.LinkType.PSV.value, en.LinkType.TCV.value]