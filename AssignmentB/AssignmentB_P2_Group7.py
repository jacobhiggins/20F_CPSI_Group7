# fire detection
# buglar detection
# power consumption (leaving electronics on, etc.)

from oracle.oracle import Oracle
oracle = Oracle()
from collections import namedtuple
import numpy as np
import time

Sensor = namedtuple('Sensor',['type','description','time_sensed','value'])

# Room 241 = Brad Campbell's Office
devices = {"c098e5700148":Sensor('power','monitor',0.0,0.0),
        "c098e5700149":Sensor('power','desktop',0.0,0.0),
        "c098e570015c":Sensor('power','mac charger',0.0,0.0),
        "c098e5700244":Sensor('power','print',0.0,0.0),
        "00888e93":Sensor('motion','near door',0.0,0.0),
        "050d69ce":Sensor('motion','on ceiling',0.0,0.0),
        "018984f9":Sensor('CO2','north wall',0.0,0.0),
        "018a33c5":Sensor('temp','near door',0.0,0.0),
        "01814dd0":Sensor('contact','on door',0.0,0.0),
        "018342dc":Sensor('contact','on window',0.0,0.0)}

def sensed_callback(msg):
    sensor_id = msg['device_id']
    sensor = devices[sensor_id]
    
    if sensor.type=='power':
        if (time.time() - sensor.time_sensed) < 60:
            return
        sensor = sensor._replace(value = msg["device_data"]["power"])
    elif sensor.type=='motion':
        sensor = sensor._replace(value = msg["device_data"]["PIR Status"])
    elif sensor.type=='CO2':
        sensor = sensor._replace(value = msg["device_data"]["Concentration_ppm"])
    elif sensor.type=='temp':
        sensor = sensor._replace(value = msg["device_data"]["Temperature_°C"])
    elif sensor.type=='contact':
        sensor = sensor._replace(value = msg["device_data"]["Contact"])
    sensor = sensor._replace(time_sensed=time.time())
    devices[sensor_id] = sensor
    print("Time: {} | Sensor Type: {} | Descriptor: {} | Value: {}".format(
        time.asctime( time.localtime(sensor.time_sensed) ),
        sensor.type,
        sensor.description,
        sensor.value))

def init_callback():
    for sensor_id in devices:
        oracle.receive(sensor_id,sensed_callback)

init_callback()

# msg = {"device_id":"c098e5700148","device_data":{"power":1.0}}
# sensed_callback(msg)

# def motion_callback(msg):
#     sensor_id = msg['device_id']
#     sensor = devices[sensor_id]
#     sensor.time_sensed = time.time()
    

# def CO2_callback(msg):
#     sensor_id = msg['device_id']
#     sensor = devices[sensor_id]
#     sensor.time_sensed = time.time()
#     sensor.value = msg['device_data']["Concentration_ppm"]

# def contact_callback(msg):
#     sensor_id = msg['device_id']
#     sensor = devices[sensor_id]
#     sensor.time_sensed = time.time()
#     sensor.value = msg['device_data']['Contact']

# def power_callback(msg):
#     sensor_id = msg['device_id']
#     sensor = devices[sensor_id]
#     sensor.time_sensed = time.time()
#     sensor.value = msg['device_data']['power']

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

