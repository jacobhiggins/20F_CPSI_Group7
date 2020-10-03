
import influxdb

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

measurements = client.query('SHOW measurements')
print(measurements)

result = client.query('SELECT value FROM Temperature_°C LIMIT 1;')
print("Result: {}".format(result))

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

temp_oct2 = client.query('SELECT value,location_specific,description FROM "Temperature_°C" WHERE time > now() - 1d')

#SELECT mean("value") FROM "Temperature_°C" WHERE  time > {} GROUP BY time(6h) ) WHERE time > '2017-01-01' GROUP BY time(24h)
import numpy as np
import pandas as pd
import datetime
import time

# Create a start and end datetime
start = "2020-10-01T00:00:00Z"
end = "2020-10-02T00:00:00Z"

# Convert to UTC format (UNIX)
T1 = time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").timetuple())
T2 = time.mktime(datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ").timetuple())

# Make a list of all rooms with temperature sensors
rooms_query = client.query('SHOW TAG VALUES FROM "Temperature_°C" WITH KEY = "location_specific"')
rooms = list(rooms_query.get_points(measurement='Temperature_°C'))
locations=[]
for room in rooms:
    locations.append(room['value'])
print(str(locations[0]))

#Can't call time in between..........
#How to use GROUP BY query in python?
temperature = client.query('SELECT value,location_specific,description FROM "Temperature_°C" WHERE time > now() - 1d')

for location in locations:
    t_location = list(temperature.get_points(measurement='Temperature_°C', tags={'location_specific': location} ))
    #Need to average for each hour in 24 hours & compare against each room
    avg_24h = []
    for value in t_location:
        avg_24h.append(value['value'])
    print(np.nanmean(avg_24h), location)

