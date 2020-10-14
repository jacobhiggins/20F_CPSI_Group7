import influxdb

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

# Define measurement desired
Freshest = "awair_score"

# Define base strings for queries
base_string = "SELECT MEAN(\"value\") FROM {} WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Define dates
date = ["2020-09-18", "2020-09-19", "2020-09-20"]

# repeat for 3 different dates
for r in range(len(date)):
    # define dictionaries for mean values 
    awair_mean_values = {}

    # repeat for each hour
    for i in range(24):
        # define time range for each hours
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)

        # construct query string
        query_string = base_string.format(Freshest, date[r], time_start_string, date[r], time_end_string)

        # mean values for each room
        result = client.query(query_string)
        result_list = result.raw["series"]

        # append dictionary where dictionary keys are room and dictionary values are mean values
        for j in range(len(result_list)):
            if i == 0 & j == 0:
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
    print("")
    print(date[r])
    print("Freshest ({}): ".format(max_room), *rooms, sep=", ")