# Author: Jacob Higgins (jdh4je)
# Assignment A, Part 2

'''
The following code evaluates what would likely be the "most comfortable room" for a particular user.
Specifically, the user puts in their ideal temperature and humidity levels.
Then, the code finds the average temperature and humidity over an entire day for each room available in the dataset.
The room that is the closest to this ideal temperature/humidity is counted as the "most comfortable room" for that day.
The code does this for all days in the past year, counting how many times each room is considered "most comfortable."
Finally, the code calculates the frequency that each room is considered ideal as a percentage of the total counts.
The code prints out the three highest rooms that are most frequently the most comfortable, for both temperature and humidity.

An extension of this code could be to construct Pareto frontiers, showing how different rooms can maximize comfort in a variety of different ways.
This code only considers temperature and humidity, but can easily be extended to other observables.
'''

import influxdb
import numpy as np

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

# Define string values for different measurements
HUMIDITY = "Humidity_%"
BRIGHTNESS = "Illumination_lx"
TEMPERATURE = "Temperature_°C" # temperature doesn't seem to work for me...
AWAIR = "awair_score"
CO2 = "co2_ppm"
VOC = "voc_ppb"

# Define base strings for queries
data_query_string_base = "SELECT MEAN(\"value\") FROM \"{}\" WHERE time > '{}T00:00:00Z' AND time < '{}T11:59:59Z' GROUP BY \"location_specific\""

ideal_temp = 19 # Celsius = 66 F
# ideal_temp = 22.2 # Celsius = 72 F
ideal_humid = 0

best_rooms_temp = {}
best_rooms_humid = {}

print("Getting data....")

for m in range(10):
    # print("2020-{0:0>2d}".format(m+1))
    for d in range(32):
        date = "2020-{0:0>2d}-{1:0>2d}".format(m+1,d+1)
        temp_query_string  = data_query_string_base.format(TEMPERATURE,date,date)
        humidity_query_string = data_query_string_base.format(HUMIDITY,date,date)
        try:
            temp_result = client.query(temp_query_string)
            humid_result = client.query(humidity_query_string)
        except:
            continue
        temp_list = temp_result.raw["series"]
        humid_list = humid_result.raw["series"]
        best_temp = ""
        temp_dist = 1000
        best_humid = ""
        humid_dist = 1000

        # Find best for temp
        for j in range(len(temp_list)):
            room = temp_list[j]["tags"]["location_specific"]
            temp = temp_list[j]["values"][0][1]
            if np.abs(temp - ideal_temp) < temp_dist:
                best_temp = room
                temp_dist = np.abs(temp-ideal_temp)
        try:
            best_rooms_temp[best_temp] += 1
        except:
            best_rooms_temp[best_temp] = 1

        # Find best for humidity
        for j in range(len(humid_list)):
            room = humid_list[j]["tags"]["location_specific"]
            humid = humid_list[j]["values"][0][1]
            if np.abs(humid - ideal_humid) < temp_dist:
                best_humid = room
                humid_dist = np.abs(temp-ideal_humid)
        try:
            best_rooms_humid[best_humid] += 1
        except:
            best_rooms_humid[best_humid] = 1
        
# print(best_rooms_temp)
# print(best_rooms_humid)

sorted_best_temps = sorted(best_rooms_temp.items(), key=lambda x: x[1],reverse=True)
sorted_best_humid = sorted(best_rooms_humid.items(), key=lambda x: x[1],reverse=True)

# Get room counts (for percentages)
best_temps_count = 0
best_humid_count = 0
for best_temp_room in sorted_best_temps:
    best_temps_count += best_temp_room[1]
for best_humid_room in sorted_best_humid:
    best_humid_count += best_humid_room[1]

# print out data

temp_string = "Most comfortable rooms by temperature: "
humid_string = "Most comfortable rooms by humidity: "

for i in range(3):
    temp_string += "({}, {:.2f}%) ".format(sorted_best_temps[i][0],sorted_best_temps[i][1]/best_temps_count)
    humid_string += "({}, {:.2f}%) ".format(sorted_best_humid[i][0],sorted_best_humid[i][1]/best_humid_count)

print("Below are the most comfortable rooms by temperature and humidity in the past year.")
print("Percentages indicated frequency of being the most comfortable room. \nThe higher the percentage, the more likely it will be comfortable.")
print("*****************")
print(temp_string)
print(humid_string)
print("*****************")