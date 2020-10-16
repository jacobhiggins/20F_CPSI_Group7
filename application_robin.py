'''
This application is meant to help users figure out which location is most ideal for an indoor plant,
based on humidity, temperature, brightness, and CO2 levels. The output is fairly basic, with
just annual averages of the four sensor readings given in a table, and sorted by highest to lowest humidity.
Based on the plant species, the sorting could be manually changed for the user to identify rooms with the ideal
variable at question. For example, some plants (e.g. desert plants) do well with low humidity.

As stated in the the following statement that's printed with the application output, a machine learning/classification
algorithm could better pinpoint the exact room by weighting each variable based on plant species. It may also be
configured to choose a specific time frame (or account for a longer average window).

Based on https://www.houseplantsexpert.com/indoor-plants-temperature-guide.html,\
 an indoor plant prefers high humidity, high CO2 levels, and temperatures ranging\
 between 15 to 24 degrees Celsius. You can consult these annual averages (2019-2020) to\
 select an ideal location depending on the plant species. Notice that the locations are\
 ranked by levels of decreasing humidity. You can choose to change the priority at the bottom of the code.\
 The locations are approximated and then averaged for estimating natural light. An improved\
 application would take account of more light level sensors at their "true" locations.\
 A classification algorithm could also be incorporated to cluster and identify the most suitable\
 conditions for an input plant species.')
'''

import influxdb
import pandas as pd
import numpy as np

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

HUMIDITY = "Humidity_%"
TEMPERATURE = "Temperature_°C"
CO2 = "co2_ppm"
BRIGHTNESS = "Illumination_lx"

############################################################################################################
# Find the optimal room for indoor plants, based on an annual average.

start_avg='2019-10-16'
end_avg='2020-10-16'

####################     CO2
query_string = '''SELECT MEAN("value") FROM "{}" WHERE time > '{}T00:00:00Z' AND time < '{}T23:59:59Z' GROUP BY "location_specific" '''.format(CO2,start_avg,end_avg)
carbon = client.query(query_string)
dataset = carbon.raw["series"]

co2_df=pd.DataFrame()
locations = []
averages = []
for i in range(len(dataset)):
    location=dataset[i]["tags"]["location_specific"]
    locations.append(location)
    average=dataset[i]["values"][0][1]
    averages.append(average)
zipped = zip(locations,averages)
a_dict = dict(zipped)
co2_df = co2_df.append(a_dict, ignore_index=True)

####################     Humidity
query_string = '''SELECT MEAN("value") FROM "{}" WHERE time > '{}T00:00:00Z' AND time < '{}T23:59:59Z' GROUP BY "location_specific" '''.format(HUMIDITY,start_avg,end_avg)
humid = client.query(query_string)
dataset = humid.raw["series"]

humid_df=pd.DataFrame()
locations = []
averages = []
for i in range(len(dataset)):
    location=dataset[i]["tags"]["location_specific"]
    locations.append(location)
    average=dataset[i]["values"][0][1]
    averages.append(average)
zipped = zip(locations,averages)
a_dict = dict(zipped)
humid_df = humid_df.append(a_dict, ignore_index=True)

####################     Temperature
query_string = '''SELECT MEAN("value") FROM "{}" WHERE time > '{}T00:00:00Z' AND time < '{}T23:59:59Z' GROUP BY "location_specific" '''.format(TEMPERATURE,start_avg,end_avg)
temperature = client.query(query_string)
dataset = temperature.raw["series"]

temp_df=pd.DataFrame()
locations = []
averages = []
for i in range(len(dataset)):
    location=dataset[i]["tags"]["location_specific"]
    locations.append(location)
    average=dataset[i]["values"][0][1]
    averages.append(average)
zipped = zip(locations,averages)
a_dict = dict(zipped)
temp_df = temp_df.append(a_dict, ignore_index=True)

####################     Brightness
query_string = '''SELECT MEAN("value") FROM "{}" WHERE time > '{}T00:00:00Z' AND time < '{}T23:59:59Z' GROUP BY "location_specific" '''.format(BRIGHTNESS,start_avg,end_avg)
bright = client.query(query_string)
dataset = bright.raw["series"]

bright_df=pd.DataFrame()
locations = []
averages = []
for i in range(len(dataset)):
    location=dataset[i]["tags"]["location_specific"]
    locations.append(location)
    average=dataset[i]["values"][0][1]
    averages.append(average)

#Define a function to group "location_specific" averages containing common room number/location name.
def renamed_avg(room_name,locations,averages):
    averages_group = []
    for location,average in zip(locations,averages):
        if room_name in location:
            averages_group.append(average)
    grouped_average = np.nanmean(averages_group)
    return grouped_average

#List of rooms for inputting into function
bright_rooms = ['201 Olsson','203 Olsson','211 Olsson','217 Olsson','241 Olsson','257 Olsson']

#Set up loop to get grouped averages for list of renamed locations.
averages_renamed = []
for room in bright_rooms:
    average = renamed_avg(room,locations,averages)
    averages_renamed.append(average)

bright_rooms_renamed = ['201 Olsson','203 Olsson','Outside 211 Olsson','Outside 217 Olsson','241 Olsson','257 Olsson']

zipped = zip(bright_rooms_renamed,averages_renamed)
a_dict = dict(zipped)
bright_df = bright_df.append(a_dict, ignore_index=True)

#Choose locations that have all four sensors (approximately): HUMIDITY, CO2, BRIGHTNESS, TEMPERATURE
temp_avg = temp_df[set(humid_df) & set(temp_df) & set(co2_df) & set(bright_df)].rename(index={0:TEMPERATURE}).T
humid_avg = humid_df[set(humid_df) & set(temp_df) & set(co2_df) & set(bright_df)].rename(index={0:HUMIDITY}).T
co2_avg = co2_df[set(humid_df) & set(temp_df) & set(co2_df) & set(bright_df)].rename(index={0:CO2}).T
bright_avg = bright_df[set(bright_df) & set(humid_df) & set(temp_df) & set(co2_df)].rename(index={0:BRIGHTNESS}).T

#Create concatenated dataframe:
plant_avg = [humid_avg, co2_avg, bright_avg, temp_avg]
plant_df = pd.concat(plant_avg, axis=1)

# Change the sorting depending on the priority for plant species: 
plant_df = plant_df.sort_values(by=[HUMIDITY], ascending=[False])

print(plant_df)
print('\nBased on https://www.houseplantsexpert.com/indoor-plants-temperature-guide.html,\
 an indoor plant prefers high humidity, high CO2 levels, and temperatures ranging\
 between 15 to 24 degrees Celsius. You can consult these annual averages (2019-2020) to\
 select an ideal location depending on the plant species.\n\nNotice that the locations are\
 ranked by levels of decreasing humidity. You can choose to change the priority at the bottom of the code.\
 The locations are approximated and then averaged for estimating natural light. An improved\
 application would take account of more light level sensors at their "true" locations.\
 A classification algorithm could also be incorporated to cluster and identify the most suitable\
 conditions for an input plant species.')




