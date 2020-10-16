# Program Description:
# The following code provides information regarding the level of safety various rooms have during an input date and time for C02, VOC, and PM25.
# The program checks each room with a sensor against the measurement, date, and time selected by the user.
# If the value for a given threshold is below the threshold, and "All Clear" status is provided.
# If the value for a given threshold is surpassed, a waring status is shown to the user.
# These thresholds were selected based on reference tables found online.

# Fullscale Program:
# This program would output every 30 min to an hour and provide real time data to a "safety officer" (SO) monitoring an area.
# Based on what information is returned, the SO can take the appropriate actions to ensure all personnel are safe.
# The full program would also more distinctly show each type of warning with a quick reference icon (i.e. check or stop sign)
# instead of categorizing the values into two level: good or bad.
# The frequency as to which the data is outputted can be increased, but care would have to be taken that there isn't an
# erroneous spike in the data to cause undue alarm.

import influxdb
from influxdb import InfluxDBClient

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1'
PASSWORD = 'ea0quoko2oajae1NiakiethaihofoseiY'
DATABASE = 'living-link-lab-open'

client = influxdb.InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

# Define measurement variables
HUMIDITY = "Humidity_%"
BRIGHTNESS = "Illumination_lx"
TEMPERATURE = "Temperature_°C"
AWAIR = "awair_score"
CO2 = "co2_ppm"
VOC = "voc_ppb"
PM25 = "pm2.5_μg/m3"

# !!!Define the date(s) desired to find the coldest room!!!
dates = ["2020-07-03"] #,"2020-07-04","2020-07-05"]

# Request what variable they would like to look at
request = input("What measurement would you like to look at? (CO2, VOC, or PM25) ")
if request=="CO2":
    measurement = CO2
elif request == "VOC":
    measurement = VOC
elif request == "PM25":
    measurement = PM25
else :
    print("")
    print("!!! You have entered an incorrect answer. Please try again. !!!")
    print("")
    exit(0)

dates = [input("What date would you like to look at? (Format: YYYY-MM-DD, i.e. 2020-07-04) ")]
print("")

print("What hour time range would you like to see data for?")
time = input("Please input an integer from 0 - 23. (i.e. 3 gives 03:00:00 to 03:59:5): ")
time = int(time)

# Print table of various levels for reference for end user based on their choice
# Source for CO2: https://www.kane.co.uk/knowledge-centre/what-are-safe-levels-of-co-and-co2-in-rooms
# Source for PM25: https://www.epa.gov/sites/production/files/2016-04/documents/2012_aqi_factsheet.pdf
# Source for VOC: https://www.tecamgroup.com/acceptable-voc-levels/

if request=="CO2":
    print("CO2 Level Reference Table:")
    print("  Value (ppm)    Description")
    print("    250 -   400: Normal in outdoor air")
    print("    400 - 1,000: Typical of occupied indoor space with")
    print("                 with good air exchange")
    print("  1,000 - 2,000: Complaints of drowsiness and poor air")
    print("  2,000 - 5,000: Headaches, sleepiness, poor concentration")
    print("                 increased heart rate, and nausea")
    print("          5,000: Workplace exposure limit (8 hour TWA)")
    print("       > 40,000: Exposure may lead to serious oxygen")
    print("                 deprivation resulting in permananet brain")
    print("                 damage, coma, evn death")
    print("")
elif request == "VOC":
    print("VOC Level Reference Table:")
    print("  Value (ppb)  Description")
    print("         < 300: Low")
    print("   300 -   500: Acceptable")
    print("   500 - 1,000: Marginal")
    print(" 1,000 - 3,000: High")
    print("")
elif request == "PM25":
    print("PM_2.5 Level Reference Table:")
    print("  Value (μg/m3)  Description")
    print("    0.0 -  12.0: Good")
    print("   12.1 -  35.4: Moderate")
    print("   35.5 -  55.4: Unhealthy for Sensitive Groups")
    print("   55.5 - 150.4: Unhealthy")
    print("  150.5 - 250.4: Very Unhealthy")
    print("  250.5 - 500.0: Hazardous")
    print("")


# Define baseline query string to get data
string = "SELECT MEAN(\"value\") FROM \"{}\" WHERE time > '{}T{}Z' AND time < '{}T{}Z' GROUP BY \"location_specific\""

# Calculate and print the desired measurement and output
for j in range(len(dates)):
    print("Date: {}".format(dates[j]))

    # Initialize the variable to store data
    desired_value = "0"
    desired_room = "Place Holder"

    # Perform calculation for each day specified
    for k in range(1):
        # Define time range
        time_start = "{0:0>2d}:00:00".format(time)
        time_end = "{0:0>2d}:59:59".format(time)

        print("Time for Range: {} to {}".format(time_start,time_end))

        # Construct query string
        query_string = string.format(measurement,dates[j],time_start,dates[j],time_end)

        # Get mean value for each room for this hour
        result = client.query(query_string)
        result_list = result.raw["series"]

        # Determine the room name and value for the measurement
        for l in range(len(result_list)):
            room = result_list[l]["tags"]["location_specific"]
            value = result_list[l]["values"][0][1]
            
            
            # Output Room Name, value, and any necessary warnings.
            if request == "CO2":
                if value < 1000:
                    warning = "All Clear!"
                else :
                    warning = "!!! PLEASE CHECK ROOM VALUE AGAINST TABLE !!!"
            elif request == "VOC":
                if value < 500:
                    warning = "All Clear!"
                else :
                    warning = "!!! PLEASE CHECK ROOM VALUE AGAINST TABLE !!!"
            elif request == "PM25":
                if value < 35.5:
                    warning = "All Clear!"
                else :
                    warning = "!!! PLEASE CHECK ROOM VALUE AGAINST TABLE !!!"

            print(" Room    :{}".format(room))
            print(" - Value :{:.2f}".format(value))
            print(" - Status:{}".format(warning))

        print("")

