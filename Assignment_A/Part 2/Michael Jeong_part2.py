#Michael Jeong
#Assignment A, Part 2

# Code description
# The following code provides users with information for the best room to study in based on room Temperature and day of the week
# The user specifies a specific date they are planning on studying
# The program compiles previous temperature data within a specified time frame (start and end dates) to calculate
# average room temperatures in various rooms and separates them by days of the week
# By calculating this, the program can then use this data on the same day of the week as the user specified study date
# and attempt to provide the room that has the closest average temperature to the ideal temperature for that particular day of the week
# The time window and ideal room temperature are set in the program but are also changeable by the user if he/she desires
# Ideal room temperature of 22.22oC is based on results from a study conducted at Westview High School in Oregon

# Further development
# This program currently only considers the temperature effect on studying efficacy but could be expanded to include
# other data measurements such as light, sound, or humidity.
# This would require consideration of the most important variable in order to optimize for multiple data measurements
# Further developments could also allow the program to consider what time of day is most ideal for a particular room
# on a particular day of the week
# More robust background information on the effects of temperature on study habits could provide better room predictions

import influxdb
from datetime import timedelta, date

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

# Define string values for different measurements
HUMIDITY = "Humidity_%"
BRIGHTNESS = "Illumination_lx"
TEMPERATURE = "Temperature_°C"
AWAIR = "awair_score"
CO2 = "co2_ppm"
VOC = "voc_ppb"

# Define base strings for queries
base_string = "SELECT MEAN(\"value\") FROM \"{}\" WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# start and end values for year, month, and day
start_numbers = [2020, 1, 10]
end_numbers = [2020, 1, 24]

# values for desired date (year, month, day)
desired_date_numbers = [2020, 10, 15]

# ideal study temperature
ideal_temp = 22.22

# start and end dates for calculating mean measruements
start_date = date(start_numbers[0], start_numbers[1], start_numbers[2])
end_date = date(end_numbers[0], end_numbers[1], end_numbers[2])
desired_date = date(desired_date_numbers[0], desired_date_numbers[1], desired_date_numbers[2])
delta = timedelta(days=1)

# dictionaries for each day of the week containing mean temperature values sorted by room
Monday_T = {}
tuesday_T = {}
wednesday_T = {}
thursday_T = {}
friday_T = {}
saturday_T = {}
sunday_T = {}
avg_T = {}

Temps = {0: Monday_T, 1: tuesday_T, 2: wednesday_T, 3: thursday_T, 4: friday_T, 5: saturday_T, 6: sunday_T}
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# fill dictionaries for each week day over for days between the start and end dates
while start_date <= end_date:
    for i in range(24):
        time_start_string = "{0:0>2d}:00:00".format(i)
        time_end_string = "{0:0>2d}:59:59".format(i)

        # construct query string
        query_string_T = base_string.format(TEMPERATURE, start_date, time_start_string, start_date, time_end_string)
        # call query
        result = client.query(query_string_T)
        result_list = result.raw["series"]
        # determine which day of the week the query data is taken from
        day_week = start_date.weekday()
        # append dictionaries accordingly based on what day of the week
        for j in range(len(result_list)):
            if day_week == 0:
                if result_list[j]["tags"]["location_specific"] not in Monday_T:
                    Monday_T[result_list[j]["tags"]["location_specific"]] = []
                Monday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 1:
                if result_list[j]["tags"]["location_specific"] not in tuesday_T:
                    tuesday_T[result_list[j]["tags"]["location_specific"]] = []
                tuesday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 2:
                if result_list[j]["tags"]["location_specific"] not in wednesday_T:
                    wednesday_T[result_list[j]["tags"]["location_specific"]] = []
                wednesday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 3:
                if result_list[j]["tags"]["location_specific"] not in thursday_T:
                    thursday_T[result_list[j]["tags"]["location_specific"]] = []
                thursday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 4:
                if result_list[j]["tags"]["location_specific"] not in friday_T:
                    friday_T[result_list[j]["tags"]["location_specific"]] = []
                friday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 5:
                if result_list[j]["tags"]["location_specific"] not in saturday_T:
                    saturday_T[result_list[j]["tags"]["location_specific"]] = []
                saturday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])
            elif day_week == 6:
                if result_list[j]["tags"]["location_specific"] not in sunday_T:
                    sunday_T[result_list[j]["tags"]["location_specific"]] = []
                sunday_T[result_list[j]["tags"]["location_specific"]].append(result_list[j]["values"][0][1])

    # move on to next day
    start_date += delta

#  determine what day of the week the desired study day is
desire_day_week = desired_date.weekday()

# find difference between average value and ideal value
for x in Temps[desire_day_week]:
    avg_T[x] = abs((sum(Temps[desire_day_week][x])/len(Temps[desire_day_week][x]))-ideal_temp)

# find minimum difference between average and ideal value and the corresponding room
min_temp_diff = 1000
min_temp_diff_room = ""
for room in avg_T:
    if avg_T[room] < min_temp_diff:
        min_temp_diff = avg_T[room]
        min_temp_diff_room = room
# temperature in the ideal room
room_temp = sum(Temps[desire_day_week][min_temp_diff_room])/len(Temps[desire_day_week][min_temp_diff_room])

# show results
print("")
print("Your chosen date for studying is {} {}:".format(days[desire_day_week],desired_date))
print("From data analyzed between {} and {}, on average, the room with the most ideal study temperature on {}'s is: {} ({}°C)".format(date(start_numbers[0], start_numbers[1], start_numbers[2]), end_date, days[desire_day_week], min_temp_diff_room, room_temp))
print("The ideal study temperature is assumed to be {}°C".format(ideal_temp))