import influxdb

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
data_query_string_base = "SELECT MEAN(\"value\") FROM {} WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Define date and observable
date = "2020-07-22"
observable = BRIGHTNESS

biggest_value_room = "(empty)"
biggest_value = 0
# For each hour
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

print("Brightest ({}): {}".format(biggest_value,biggest_value_room))