from oracle.oracle import Oracle
oracle = Oracle()

def on_receive_power_data(msg):
    # access the device_data field to obtain sensor readings
    power_value = msg['device_data']['power']
    print(power_value, flush=True)

def on_receive_temp_data(msg):
    print(msg, flush=True)

# We have the device ids of the two sensors listed here
power_meter_id = "c098e5700244"
temp_humidity_sensor_id = "018a29cc"

oracle.receive(power_meter_id, on_receive_power_data)
oracle.receive(temp_humidity_sensor_id, on_receive_temp_data)

