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

for r in range(len(date)):
    # define dictionaries for mean values and max mean values for each room and hour
    awair_mean_values = {}
    awair_max_values = {}

    # define time range for first hour (only could do this process by doing first hour separately from the remaining 23 - probably not most efficient)
    time_start_string = "{0:0>2d}:00:00".format(1)
    time_end_string = "{0:0>2d}:59:59".format(1)

    #  construct query string
    query_string = base_string.format(Freshest,date[r],time_start_string,date[r],time_end_string)

    # get mean values for each room at each hour
    result = client.query(query_string)
    result_list = result.raw["series"]

    # create dictionary where keys are rooms and values are list of mean values
    for j in range(len(result_list)):
        awair_mean_values[result_list[j]["tags"]["location_specific"]] = []
        awair_mean_values[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])

    # repeat process for remaining 23 hours
    for i in range(23):
        # define time range for remaining 23 hours
        time_start_string = "{0:0>2d}:00:00".format(i+1)
        time_end_string = "{0:0>2d}:59:59".format(i+1)

        # construct query string
        query_string = base_string.format(Freshest, date[r], time_start_string, date[r], time_end_string)

        # mean values for each room for remaining 23 hours
        result = client.query(query_string)
        result_list = result.raw["series"]

        # append dictionary to include all mean values for each hour
        for j in range(len(result_list)):
            awair_mean_values[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])

    # append second dictionary (awair_max_values) to only include maximumm mean values
    for x in awair_mean_values:
        awair_max_values[x] = max(awair_mean_values[x])

    # maximum awair value
    max_room = max(awair_max_values.values())

    # list of rooms that contain maximum awair value
    rooms = []
    for room in awair_max_values:
        if awair_max_values[room] == max_room:
            rooms.append(room)

    # print winning value and corresponding rooms
    print("Freshest on {} ({}): ".format(date[r], max_room), *rooms, sep=", ")






