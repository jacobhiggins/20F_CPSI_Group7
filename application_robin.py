import influxdb
import pandas as pd

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

HUMIDITY = "Humidity_%"
TEMPERATURE = "Temperature_°C"
CO2 = "co2_ppm"

############################################################################################################
# Find the optimal room for indoor plants, based on a user-defined average. Here, we use an annual average.

# Define time span to average. 
start_avg='2019-10-16'
end_avg='2020-10-16'

#CO2
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

#Humidity
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

#Temperature
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

#Choose locations that have all three sensors (HUMIDITY, CO2, TEMPERATURE)
temp_avg = temp_df[set(humid_df) & set(temp_df) & set(co2_df)].rename(index={0:'Temperature (C)'}).T
humid_avg = humid_df[set(humid_df) & set(temp_df) & set(co2_df)].rename(index={0:'Humidity (%)'}).T
co2_avg = co2_df[set(humid_df) & set(temp_df) & set(co2_df)].rename(index={0:'CO2 (ppm)'}).T
plant_avg = [humid_avg, co2_avg, temp_avg,]

plant_df = pd.concat(plant_avg, axis=1)
plant_df = plant_df.sort_values(by=['Humidity (%)', 'CO2 (ppm)', 'Temperature (C)'], ascending=[False,True,True])
print(plant_df)

print('\n Based on https://www.houseplantsexpert.com/indoor-plants-temperature-guide.html,\
 an indoor plant prefers high humidity, high CO2 levels, and temperatures ranging\
 between 15 to 24 degrees Celsius. Based on these annual averages (2019-2020), the top rows should\
 indicate ideal locations for an indoor plant. *Results may vary depending on species & available sunlight.*')