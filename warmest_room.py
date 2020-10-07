
import influxdb

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

#0.A
measurements = client.query('SHOW MEASUREMENTS')
print(measurements)
#0.B
gateway_Awair = client.query('SHOW TAG VALUES FROM "awair_score" WITH KEY = "gateway_id"')
print("Result: {}".format(gateway_Awair))
#0.C Not sure how to call measurement with specific tag...
device = measurements.get_series(tags={'device_id': '05060dd8'})
print(device)
client.query(tags={'device_id':'05060dd8'})

#Tag keys
result = client.query('SHOW TAG KEYS FROM "Temperature_°C"')
result.raw
#Tag values from tag key
desc = client.query('SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "description"')
desc.raw
dclass = client.query('SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "device_class"')
dclass.raw
dID = client.query('SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "device_id"')

#Field Keys
fields = client.query('SHOW FIELD KEYS FROM "Temperature_°C"')
fields.raw

#Field Values
values = client.query('SELECT value FROM "Temperature_°C"  LIMIT 1;')
values.raw

import numpy as np
import pandas as pd
'''
Plan:
0. User defines the day; Convert timestamps
1. Create database with columns of rooms
2. Get mean value for each hour
3. Store value chronologically 00 to 24 in each row
4. Find index of highest value
5. Index of room
'''

####################################################################################################################
#WARMEST ROOM OF THE DAY IN A SINGLE HOUR (AVERAGED PER HOUR)

# Select the day: YYYY-MM-DD
days = ["2020-07-02",
        "2020-08-02",
        "2020-09-02"]

# Make a list of all rooms with sensors
rooms_query = client.query('''SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "location_specific"''')
rooms = list(rooms_query.get_points(measurement="Temperature_°C"))
locations=[]
for room in rooms:
    locations.append(room['value'])
#print((len(locations)))

#Base query string
base = '''SELECT value,location_specific,description FROM "Temperature_°C" WHERE time > '{}T{}Z' AND time < '{}T{}Z' '''

for day in days:
    #Pandas dataframe with rooms
    temperature_df=pd.DataFrame(columns = locations)
    for i in range(24):
        # Get start and stop time for querying
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)
        single_avg_values = []
        temperature = client.query(base.format(day,time_start_string,day,time_end_string))
        #For each location
        for location in locations:
            t_location = list(temperature.get_points(measurement="Temperature_°C", tags={'location_specific': location} ))
        #Average all queried temperature values
            for i in range(len(locations)):
                values_24h = []
                for value in t_location:
                    values_24h.append(value['value'])
                single_avg_value = np.nanmean(values_24h)
            single_avg_values.append(single_avg_value)
        zipped = zip(locations,single_avg_values)
        a_dict = dict(zipped)
        temperature_df = temperature_df.append(a_dict, ignore_index=True)

    #Find warmest temperature in the day of an hour & its index
    warmest_temp = (temperature_df.max(axis=1)).max()
    warmest_tempid = (temperature_df.max(axis=1)).idxmax()

    #Find warmest room in the day of an hour with its index
    warmest_room = (temperature_df.idxmax(axis=1))[warmest_tempid]

    #Print answer
    print(''' {}\n Warmest ({}°C): {}\n\n '''.format(day,warmest_temp,warmest_room))


####################################################################################################################
#WARMEST ROOM OF THE DAY (AVERAGED 24 HOURS)

# Select the day: YYYY-MM-DD
date='2020-07-02'

# Make a list of all rooms with temperature sensors
rooms_query = client.query('SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "location_specific"')
rooms = list(rooms_query.get_points(measurement='Temperature_°C'))
locations=[]
for room in rooms:
    locations.append(room['value'])
#print((len(locations)))

#Pandas dataframe with rooms
temperature_df=pd.DataFrame(columns = locations)

#How to use GROUP BY query in python? Need to get hourlies
single_avg_values = []
temperature = client.query(''' SELECT value,location_specific,description FROM "Temperature_°C" WHERE time> '{}T00:00:00Z' AND time < '{}T23:59:59Z' '''.format(date,date))
#For each location
for location in locations:
    t_location = list(temperature.get_points(measurement='Temperature_°C', tags={'location_specific': location} ))
   # Average all queried temperature values
    for i in range(len(locations)):
        values_24h = []
        for value in t_location:
            values_24h.append(value['value'])
        single_avg_value = np.nanmean(values_24h)
    single_avg_values.append(single_avg_value)

zipped = zip(locations,single_avg_values)
a_dict = dict(zipped)
temperature_df = temperature_df.append(a_dict, ignore_index=True)

warmest_temp = temperature_df.max(axis=1)
warmest_room = temperature_df.idxmax(axis=1)

print(warmest_temp[0])
print(warmest_room[0])



####################################################################################################################
# Combined code with Jacob's

# Make a list of all rooms with sensors
rooms_query = client.query('SHOW TAG VALUES FROM "Illumination_lx" WITH KEY = "location_specific"')
rooms = list(rooms_query.get_points(measurement="Illumination_lx"))
locations=[]
for room in rooms:
    locations.append(room['value'])
#print((len(locations)))

#Pandas dataframe with rooms
bright_df=pd.DataFrame(columns = locations)

base = "SELECT value,location_specific,description FROM Illumination_lx WHERE time > '{}T{}Z' AND time < '{}T{}Z'"
day = "2020-07-02"

for i in range(24):
    # Get start and stop time for querying
    time_start_string = "{0:0>2d}:00:00".format(i)
    time_end_string = "{0:0>2d}:59:59".format(i)
    single_avg_values = []
    temperature = client.query(base.format(day,time_start_string,day,time_end_string))
    #For each location
    for location in locations:
        t_location = list(temperature.get_points(measurement='Illumination_lx', tags={'location_specific': location} ))
    # Average all queried temperature values
        for i in range(len(locations)):
            values_24h = []
            for value in t_location:
                values_24h.append(value['value'])
            single_avg_value = np.nanmean(values_24h)
        single_avg_values.append(single_avg_value)
    zipped = zip(locations,single_avg_values)
    a_dict = dict(zipped)
    bright_df = bright_df.append(a_dict, ignore_index=True)

#print(bright_df)
brightest_temp = (bright_df.max(axis=1)).max()
brightest_tempid = (bright_df.max(axis=1)).idxmax()

brightest_room = (bright_df.idxmax(axis=1))[brightest_tempid]

print(brightest_temp, brightest_room)
