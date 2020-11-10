from oracle.oracle import Oracle
from collections import namedtuple
import numpy as np

# room1 = 257 Olsson
# room2 = 241 Olsson
# room3 = 211 Olsson

class MyOracle(Oracle):

    # Callback functions for sensor readings
    def motionCallback(msg):
        print("motion callback")
        self.values[0] = msg["device_data"]["Supply voltage (OPTIONAL)_V"]
    def doorCallback(msg):
        print("door callback")
        self.values[1] = msg["device_data"]["Contact"]


    def __init__(self):
        super().__init__()
        self.sensor_types = ["motion","door"]
        self.num_sensors = 2
        self.num_rooms = 3
        self.ids = []
        self.ids.append(["050d5e42","00888e93","05083a3c"]) # motion sensor ids
        self.ids.append(["018330f8","01814dd0","1834188"]) # door sensor ids
        self.callbacks = [self.doorCallback,self.motionCallback]
        self.values = np.zeros([self.num_rooms,self.num_sensors]) # sensor values
        self.times = np.zeros([self.num_rooms,self.num_sensors])

    def receive_data(self,device_type,room_num):
        func_num = 0
        ids = 0
        for i in range(len(self.sensor_types)):
            if device_type==self.sensor_types[i]:
                ids = self.ids[i]
                func_num = i
        if ids==0:
            print("ERROR\nPlease use either \"motion\" or \"door\" for device type.")
            return
        sensor_id = ids[room_num]
        super.receive(sensor_id,self.callbacks[i])

x = MyOracle()
x.receive_data("door",1)
x.receive_data("motion",1)
print("finished receiving")


    



