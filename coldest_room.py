import influxdb
from influxdb import InfluxDBClient

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

# Find and print the name(s) of the measurment(s) availables
print("")
print("Measurement Name(s):")
result = client.query("SHOW MEASUREMENTS")
result_list = result.raw["series"]
for i in range(len(result_list[0]["values"])):
    measurement_list = result_list[0]["values"][i][0]
    print("{}".format(measurement_list))
print("")

# !!!Define the date(s) desired to find the coldest room!!!
dates = ["2020-07-03","2020-07-04","2020-07-05"]

# !!!Define the measurement desired!!!
measurement = "Temperature_°C"

# Define baseline query string to get data
string = "SELECT MEAN(\"value\") FROM \"{}\" WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Calculate and print the desired measurement and output
for j in range(len(dates)):
    print(dates[j])

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
    print("Coldest ({:.2f}): Room {}".format(desired_value,desired_room))
    print("")