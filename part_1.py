import influxdb
import numpy as np
import pandas as pd

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

#Define dates!
dates = ["2020-04-03","2020-05-04","2020-07-05"]


################# Brightest (Jacob)
# Define string values for different measurements
HUMIDITY = "Humidity_%"
BRIGHTNESS = "Illumination_lx"
TEMPERATURE = "Temperature_°C"
AWAIR = "awair_score"
CO2 = "co2_ppm"
VOC = "voc_ppb"

# Define base strings for queries
data_query_string_base = "SELECT MEAN(\"value\") FROM {} WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Define date and observable
observable = BRIGHTNESS

for date in dates:
    biggest_value_room = "(empty)"
    biggest_value = 0
    for i in range(24):
        # Get start and stop time for querying
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)
        # Construct query string
        query_string = data_query_string_base.format(observable,date,time_start_string,date,time_end_string)
        # Get mean value for each room for this hour
        result = client.query(query_string)
        # Get a list of all results (must do this to get room name with hourly mean)
        result_list = result.raw["series"]
        for j in range(len(result_list)):
            room = result_list[j]["tags"]["location_specific"]
            value = result_list[j]["values"][0][1]
            if value > biggest_value:
                biggest_value_room = room
                biggest_value = value
    print(date)
    print("Brightest ({:.2f}): {}".format(biggest_value,biggest_value_room))


print("")
################# Warmest (Robin)
# Make a list of all rooms with sensors
rooms_query = client.query('''SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "location_specific"''')
rooms = list(rooms_query.get_points(measurement="Temperature_°C"))
locations=[]
for room in rooms:
    locations.append(room['value'])

#Base query string
base = '''SELECT value,location_specific,description FROM "Temperature_°C" WHERE time > '{}T{}Z' AND time <= '{}T{}Z' '''

#Loop for each day
for day in dates:
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
    print('''{}\nWarmest ({:.2f}°C): {} at Hour {} UTC'''.format(day,warmest_temp,warmest_room,warmest_tempid))


print("")
################# Coldest (Spencer)
# !!!Define the measurement desired!!!
measurement = "Temperature_°C"

# Define baseline query string to get data
string = "SELECT MEAN(\"value\") FROM \"{}\" WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Calculate and print the desired measurement and output
for j in range(len(dates)):

    # Initialize the variable to store data
    desired_value = "0"
    desired_room = "Place Holder"

    # Perform calculation for each day specified
    for k in range(24):
        # Define time range
        time_start = "{0:0>2d}:00:00".format(k)
        time_end = "{0:0>2d}:59:59".format(k)

        # Construct query string
        query_string = string.format(measurement,dates[j],time_start,dates[j],time_end)

        # Get mean value for each room for this hour
        result = client.query(query_string)
        result_list = result.raw["series"]

        # Determine the room name and value for the "winning" room
        for l in range(len(result_list)):
            room = result_list[l]["tags"]["location_specific"]
            value = result_list[l]["values"][0][1]

            # Initialize the room and value storage variable w/ first value pulled
            if (k==0) and (l==0):
                desired_room = room
                desired_value = value

            # !!!Modify the else if statement to define if you want largest or smallest value!!!
            if value < desired_value:
                desired_room = room
                desired_value = value

    # Print the winning value and associated room    
    print(dates[j])
    print("Coldest ({:.2f}): Room {}".format(desired_value,desired_room))


print("")
################# Freshest (Michael)
# Define measurement desired
Freshest = "awair_score"

# Define base strings for queries
base_string = "SELECT MEAN(\"value\") FROM {} WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# repeat for 3 different dates
for r in range(len(dates)):
    # define dictionaries for mean values
    awair_mean_values = {}

    # repeat for each hour
    for i in range(24):
        # define time range for each hours
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)

        # construct query string
        query_string = base_string.format(Freshest, dates[r], time_start_string, dates[r], time_end_string)

        # mean values for each room
        result = client.query(query_string)
        result_list = result.raw["series"]

        # append dictionary where dictionary keys are room and dictionary values are mean values
        for j in range(len(result_list)):
            if result_list[j]["tags"]["location_specific"] not in awair_mean_values:
                awair_mean_values[result_list[j]["tags"]["location_specific"]] = []
            awair_mean_values[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])

    # find maximum awair value
    max_room = 0
    for room in awair_mean_values:
        for i in range(len(awair_mean_values[room])):
            if awair_mean_values[room][i] > max_room:
                max_room = awair_mean_values[room][i]

    # list of rooms that contain maximum awair value
    rooms = []
    for room in awair_mean_values:
        if max_room in awair_mean_values[room]:
            rooms.append(room)

    # print winning value and corresponding rooms
    print(dates[r])
    print("Freshest ({:.2f}): ".format(max_room), *rooms, sep=", ")