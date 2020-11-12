# fire detection
# buglar detection
# power consumption (leaving electronics on, etc.)

# from oracle.oracle import Oracle
# oracle = Oracle()
from collections import namedtuple
import numpy as np
import time

Sensor = namedtuple('Sensor',['sensor_type','description','time_sensed','value'])

# Room 241 = Brad Campbell's Office
devices = {"c098e5700148":Sensor('power','monitor',0.0,0.0),
        "c098e5700149":Sensor('power','desktop',0.0,0.0),
        "c098e570015c":Sensor('power','mac charger',0.0,0.0),
        "c098e5700244":Sensor('power','print',0.0,0.0),
        "00888e93":Sensor('motion','near door',0.0,0.0),
        "050d69ce":Sensor('motion','on ceiling',0.0,0.0),
        "018984f9":Sensor('CO2','north wall',0.0,0.0),
        "018a33c5":Sensor('temp&humidity','near door',0.0,0.0),
        "01814dd0":Sensor('contact','on door',0.0,0.0),
        "018342dc":Sensor('contact','on window',0.0,0.0)}

# # Room 241 = Brad Campbell's Office
# devices = {"c098e5700148":["power","monitor"],
#         "c098e5700149":["power","desktop",],
#         "c098e570015c":["power","Mac charger"],
#         "c098e5700244":["power","black-white printer"],
#         "00888e93":["motion","near door"],
#         "050d69ce":["motion","on ceiling"],
#         "018984f9":["CO2","north wall"],
#         "018a33c5":["Temp&Humidity","near door"],
#         "01814dd0":["contact","on door"],
#         "018342dc":["contact","on window"]}

