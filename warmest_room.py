import influxdb
import numpy as np
import pandas as pd

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

'''
Plan:
0. User defines the day
1. Create dataframe
2. Get mean value for each hour
3. Store value chronologically 00 to 24 in each row
4. Find index of highest value
5. Index of room
'''
####################################################################################################################
#WARMEST ROOM OF THE DAY IN A SINGLE HOUR (AVERAGED PER HOUR)

# Select the days (YYYY-MM-DD) with user input
print("Please answer the following prompts (x3) in YYYY-MM-DD format (no quotes required):\n")
days=[]
for i in range(3):
    day = input("Which day would you like to know about? ")
    days.append(day)

# Make a list of all rooms with sensors
rooms_query = client.query('''SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "location_specific"''')
rooms = list(rooms_query.get_points(measurement="Temperature_°C"))
locations=[]
for room in rooms:
    locations.append(room['value'])

#Base query string
base = '''SELECT value,location_specific,description FROM "Temperature_°C" WHERE time > '{}T{}Z' AND time <= '{}T{}Z' '''

#Loop for each day
for day in days:
    #New Pandas dataframe
    temperature_df=pd.DataFrame()
    for i in range(24):
        # Get start and stop time for querying
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)
        single_avg_values = []
        temperature = client.query(base.format(day,time_start_string,day,time_end_string))
        #For each location...
        for location in locations:
            t_location = list(temperature.get_points(measurement="Temperature_°C", tags={'location_specific': location} ))
        #average all queried temperature values
            for i in range(len(locations)):
                values_24h = []
                for value in t_location:
                    values_24h.append(value['value'])
                single_avg_value = np.nanmean(values_24h)
            single_avg_values.append(single_avg_value)
        #Create a dataframe
        zipped = zip(locations,single_avg_values)
        a_dict = dict(zipped)
        temperature_df = temperature_df.append(a_dict, ignore_index=True)

    #Find warmest temperature in the day of an hour & its index
    warmest_temp = (temperature_df.max(axis=1)).max()
    warmest_tempid = (temperature_df.max(axis=1)).idxmax()

    #Find warmest room in the day of an hour with its index
    warmest_room = (temperature_df.idxmax(axis=1))[warmest_tempid]

    #Print answer
    print('''{}\n Warmest ({}°C): {} at Hour {} UTC\n\n '''.format(day,warmest_temp,warmest_room,warmest_tempid))