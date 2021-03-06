# Group 7
# Assignment B
# Authors: Jacob Higgins, Michael Jeong, Robin Kim, Spencer Stebbins

# Description: Proof of conception for personalized room data tracking app.
# Coded are two functionalities: power consumption tracker and burglar alarm
# The room used is Olsson 241 (Professor Cambell's Office) since it has the most devices in it.

# Burglar alarm: User can set times alarm is armed/unarmed. During this time,
# the program looks for different attack vectors including:
#  - Open door or window (contact sensor)
#  - Temperature/CO2 above certain levels
#  - Motion sensor
# If any two of these are triggered, then the user is notified and the police are called (not really).

# Power consumption: A user can track his/her power usage and compare power usage between devices.

from oracle.oracle import Oracle
oracle = Oracle()
from collections import namedtuple
import numpy as np
import time

HOUR_START = 17 # Alarm armed at 5 p.m.
HOUR_STOP = 7 # Alarm unarmed at 7 a.m.
NORMAL_NIGHT_TEMP = 25 # Temperature above which a person is present at night
NORMAL_NIGHT_CO2 = 670 # CO2 level above which a person can be detected

Sensor = namedtuple('Sensor',['type','description','time_sensed','value'])

# power used by indivdual things [monitor, desktop, mac charger, printer]
power_usage = [0,0,0,0]
# total power usage of all 4 combined
total_power = 0
last_power_time = 0

# Room 241 = Brad Campbell's Office
devices = {"c098e5700148":Sensor('power','monitor',0.0,0.0),
        "c098e5700149":Sensor('power','desktop',0.0,0.0),
        "c098e570015c":Sensor('power','mac charger',0.0,0.0),
        "c098e5700244":Sensor('power','print',0.0,0.0),
        "00888e93":Sensor('motion','near door',0.0,0.0),
        "050d69ce":Sensor('motion','on ceiling',0.0,0.0),
        "018984f9":Sensor('CO2','north wall',0.0,0.0),
        "018a33c5":Sensor('temp','near door',0.0,0.0),
        "01814dd0":Sensor('contact','on door',0.0,-1.0),
        "018342dc":Sensor('contact','on window',0.0,-1.0)}

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
    power_use(sensor)
    buglar_alarm()

def init_callback():
    for sensor_id in devices:
        oracle.receive(sensor_id,sensed_callback)

def buglar_alarm():
    local_time = time.localtime(time.time())
    hour = local_time.tm_hour
    # If within time that the alarm is armed
    if hour < HOUR_STOP or hour > HOUR_START:
        attack_vectors = []
        attack_times = []
        # Check if motion is detected
        for sensor_id in devices:
            sensor = devices[sensor_id]
            if sensor.type=='motion' and abs(sensor.value-1)<0.0001:
                alert = True
                threat_vector = "Motion sensed within room."
                attack_vectors.append(threat_vector)
                attack_times.append(sensor.time_sensed)
            elif sensor.type=='temp' and sensor.value > NORMAL_NIGHT_TEMP:
                alert = True
                threat_vector = "Temperature above normal value."
                attack_vectors.append(threat_vector)
                attack_times.append(sensor.time_sensed)
            elif sensor.type=='contact' and abs(sensor.value)<0.001:
                alert = True
                threat_vector = "Contact was released for sensor {}.".format(sensor.description)
                attack_vectors.append(threat_vector)
                attack_times.append(sensor.time_sensed)
            elif sensor.type=='CO2' and sensor.value > NORMAL_NIGHT_CO2:
                alert = True
                threat_vector = "CO2 levels above normal value."
                attack_vectors.append(threat_vector)
                attack_times.append(sensor.time_sensed)
            
            if len(attack_times)==2:
                if abs(attack_times[0]-attack_times[1]) < 5*60:
                    print("ALERT! Possible buglar is inside office. Calling police now.")
                    print("Reasons for alert:")
                    print(attack_vectors[0])
                    print(attack_vectors[1])

# power use of electronics
def power_use(sensor):
    global power_usage
    global total_power
    global last_power_time
    # add on amount of power for each componenet individually
    if sensor.type == 'power':
        if sensor.description == 'monitor':
            power_usage[0] += float(sensor.value)
        elif sensor.description == 'desktop':
            power_usage[1] += float(sensor.value)
        elif sensor.description == 'mac charger':
            power_usage[2] += float(sensor.value)
        elif sensor.description == 'print':
            power_usage[3] += float(sensor.value)
    # total power usage
    total_power = sum(power_usage)
    # percentages for each component
    monitor_power = 100 * (power_usage[0] / total_power)
    desktop_power = 100 * (power_usage[1] / total_power)
    charger_power = 100 * (power_usage[2] / total_power)
    print_power = 100 * (power_usage[3] / total_power)
    # print output
    if (time.time() - last_power_time) > 5*60:
        print("power usage breakdown:{:.2f}% monitor | {:.2f}% desktop | {:.2f}% mac charger | {:.2f}% printer".format(monitor_power,
                                                                                              desktop_power,
                                                                                              charger_power,
                                                                                              print_power))
        last_power_time = time.time()

init_callback()