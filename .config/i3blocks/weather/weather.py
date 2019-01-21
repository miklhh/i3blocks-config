#!/bin/python
import requests
import xml.etree.ElementTree as ET
import datetime
import sys
import time


# Good to have data + funky emojicons.
date = datetime.datetime.now().strftime("%Y-%m-%d")
sun_rise_emoji = "\U0001F305"                 # Day         #Night
weather_types = { "Fair"                : ["\U0001F324", "\U0001F319"],
                  "Partly cloudy"       : ["\U000026C5", "\U00002601"],
                  "Clear sky"           : ["\U0001F31E", "\U0001F319"],
                  "Cloudy"              : ["\U00002601", "\U00002601"],
                  "Light rain"          : ["\U0001F326", "\U0001F327"],
                  "Rain"                : ["\U0001F327", "\U0001F327"],
                  "Heavy Rain"          : ["\U0001F327", "\U0001F327"],
                  "Snow"                : ["\U00002744", "\U00002744"],
                  "Heavy snow"          : ["\U00002744", "\U00002744"],
                  "Foggy"               : ["\U0001F32B", "\U0001F32B"],
                  "Light snow showers"  : ["\U00000000", "\U00000000"]}



# Command line argument. Get desiered forecasts.
forecasts = 0
delay = 0
if len(sys.argv) == 2:
    forecasts = int(sys.argv[1])
elif len(sys.argv) == 3:
    forecasts = int(sys.argv[1])
    delay = int(sys.argv[2])
else:
    print("Error, usage: \"" + sys.argv[0] + " <forecasts> (<delay second>)\"")
    exit()

# Delay. The user might find it desiereble to sleep for some time, to ex. wait
# for an internet connection before making the request.
time.sleep(delay)

# Get the weatherdata from YR.
yr_url = "https://www.yr.no/place/Sverige/%C3%96sterg%C3%B6tland/Link%C3%B6ping/forecast.xml"
yr_response = 0
try:
    yr_response = requests.get(yr_url)
except requests.ConnectionError:
    print("Missing \U0001F4F6")
    exit()
yr_xml_root = 0
if yr_response.status_code != 200:
    print("Error: YR status code " + str(yr_response.status_code))
    exit()
else:
    yr_xml_root = ET.fromstring(yr_response.text)


# Parse the location.
location = yr_xml_root.find("location")
location_name = location.find("name").text
location_country = location.find("country").text


# Parse the sun rise and set time.
sun_rise_time = yr_xml_root.find("sun").attrib.get("rise");
sun_rise_time = sun_rise_time[ sun_rise_time.find('T') + 1 : len(sun_rise_time) - 3 ]
sun_set_time = yr_xml_root.find("sun").attrib.get("set");
sun_set_time = sun_set_time[ sun_set_time.find('T') + 1 : len(sun_set_time) - 3 ]


# Get todays weather.
if forecasts < 1:
    # No forecast. Exit.
    exit()

elif forecasts == 1:
    # One forecast. The user wants it on short form.
    forecast = yr_xml_root.find("forecast")
    forecast_tabular = forecast.find("tabular")
    forecast_now = forecast_tabular.find("time")
    temp = forecast_now.find("temperature").attrib.get("value")
    weather = forecast_now.find("symbol").attrib.get("name")
    precipitation = forecast_now.find("precipitation").attrib.get("value");

    # Daytime or nighttime?
    sun_rise = datetime.datetime.strptime(sun_rise_time, "%H:%M")
    sun_set = datetime.datetime.strptime(sun_set_time, "%H:%M")
    now = datetime.datetime.now()
    night = 1 if now.time() < sun_rise.time() or sun_set.time() < now.time() else 0

    # Print the weather.
    if weather in weather_types:
        print(weather + ": " + weather_types.get(weather)[night] + " ", end="")
    else:
        print(weather + " ", end="")

    # Print the temperature.
    print(temp + "\u00B0")

    # Print sun rise time.
    print ("[" + sun_rise_time + " " + sun_rise_emoji + " " + sun_set_time + "]", end=" ")

    # Print the precipitation.
    umbrealla_clear = "\u2602"
    umbrealla_rain = "\u2614"
    raindrop = "\U0001F6BF"
    print("[" + raindrop + " " + precipitation + "mm" + "]")

else:
    # Print weather meta data.
    print("Weather from YR.no for: " + location_name + ", " + location_country + ".")

    # More than one forecast. The user wants detailed data.
    forecast = yr_xml_root.find("forecast")
    forecast_tabular = forecast.find("tabular")

    # Find max padding from weather.
    max_padding = 0
    iteration = 1
    for entry in forecast_tabular:
        length = len(entry.find("symbol").attrib.get("name"))
        if length > max_padding:
            max_padding = length
        if iteration == forecasts: break
        else: iteration += 1
    max_padding_str = '{0:<' + str(max_padding + 2) + "}"

    # Iterate over at least 'forecasts' number of table entries, but not more
    # times than the number of entries in the XML document.
    iteration = 1
    for entry in forecast_tabular:

        # Get table information.
        time_from = entry.attrib.get("from")
        time_to = entry.attrib.get("to")
        temp = entry.find("temperature").attrib.get("value")
        weather = entry.find("symbol").attrib.get("name")
        wind_direction = entry.find("windDirection").attrib.get("code")
        wind_speed = entry.find("windSpeed").attrib.get("mps")
        pressure = entry.find("pressure").attrib.get("value")
        precipitaion = entry.find("precipitation").attrib.get("value")
       
        # Print time information.
        print(time_from[:10] + " " + time_from[ 11 : len(time_from) - 3 ] + " -> ", end="")
        print(  time_to[:10] + " " +   time_to[ 11 : len(time_to)   - 3 ] + ": ",   end="")
        print('{0:>3}'.format(temp) + "\xb0C" + ", ", end="")
        print(max_padding_str.format(weather + ", "), end="")
        print("Wind: " + '{0:>4}'.format(wind_speed) + " m/s " + '{0:>3}'.format(wind_direction))

        # Test for exit.
        if iteration == forecasts: break
        else: iteration += 1

