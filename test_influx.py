import influxdb

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

result = client.query('SELECT value FROM voc_ppb LIMIT 1;')
print("Result: {}".format(result))

x = 6
print(x)

#Robin was here.
#Spencer was here


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


####################################################################################################################
# Combined Robin's code with Jacob's for validation

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
