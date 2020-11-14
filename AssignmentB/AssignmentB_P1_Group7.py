# Group 7
# Assignment B
# Authors: Jacob Higgins, Michael Jeong, Robin Kim, Spencer Stebbins

from oracle.oracle import Oracle
oracle = Oracle()
import numpy as np
import time

# room1 = 257 Olsson
# room2 = 241 Olsson
# room3 = 211 Olsson

num_rooms = 3
num_sensors = 2

# maximum seconds between door and motion when something is considered "recent"
# i.e. if the motion sensor was triggered <recent_time> seconds within door sensor, then the two are correlated
recent_time = 20.0*60

ids_dict = {"050d5e42":["motion","257 Olsson"],
            "00888e93":["motion","241 Olsson"],
            "05083a3c":["motion","211 Olsson"],
            "018330f8":["door","257 Olsson"],
            "01814dd0":["door","241 Olsson"],
            "01834188":["door","211 Olsson"]}

rooms = {}

# Binary classification, keeps track of recent motion
# 0 = no motion recently
# 1 = motion detected recently
rooms.update({"257 Olsson": [0.0,0.0]})
rooms.update({"241 Olsson": [0.0,0.0]}) 
rooms.update({"211 Olsson": [0.0,0.0]})

def doorCallback(msg):
    time.sleep(5)
    sensor_id = msg['device_id']
    # print("sensor_id: {}".format(sensor_id))
    room_name = ids_dict[sensor_id][1]
    t = time.time()
    t_string = time.asctime( time.localtime(t) )
    print("{}: door sensor triggered at time {}".format(room_name,t_string))
    time_motion_sensed = rooms[room_name][0]
    value_motion_sensed = rooms[room_name][1]
    if (t - time_motion_sensed) < recent_time and abs(value_motion_sensed-1)<0.001:
        print("Motion recently detected in {}!".format(room_name))
    else:
        print("Motion NOT recently detected in {}.".format(room_name))

def motionCallback(msg):
    sensor_id = msg['device_id']
    # print("sensor_id: {}".format(sensor_id))
    room_name = ids_dict[sensor_id][1]
    t = time.time()
    t_string = time.asctime( time.localtime(t) )
    rooms[room_name][0] = t # time motion sensor triggered
    rooms[room_name][1] = msg['device_data']['PIR Status'] # value of motion sensor
    
    print("{}: motion sensor triggered at time {}".format(room_name,t_string))

callbacks = [doorCallback,motionCallback]


def init_receive_data():
    for sensor_id in ids_dict:
        if ids_dict[sensor_id][0]=="motion":
            oracle.receive(sensor_id,callbacks[1])
            # print(1)
        elif ids_dict[sensor_id][0]=="door":
            oracle.receive(sensor_id,callbacks[0])
            # print(1)

init_receive_data()