#!/bin/python
import requests
import xml.etree.ElementTree as ET
import datetime
import sys
import time
import os

# Forecast URL.
yr_url = "https://www.yr.no/place/Sverige/%C3%96sterg%C3%B6tland/Link%C3%B6ping/forecast.xml"


# Good to have data + funky emojicons.
forecast_file = os.path.dirname(os.path.realpath(__file__)) + "/forecast.xml"
date = datetime.datetime.now().strftime("%Y-%m-%d")
                                          # Day   #Night
weather_types = { "Fair"                : ["☀️",   "🌙"],
                  "Partly cloudy"       : ["⛅",  "☁️"],
                  "Clear sky"           : ["☀️",   "🌙"],
                  "Cloudy"              : ["☁️",   "☁️"],
                  "Light rain"          : ["🌧️",  "🌧️"],
                  "Rain"                : ["🌧️",  "🌧️"],
                  "Heavy Rain"          : ["🌧️",  "🌧️"],
                  "Snow"                : ["🌨️",  "🌨️"],
                  "Heavy snow"          : ["🌨️",  "🌨️"],
                  "Foggy"               : ["🌫️",  "🌫️"],
                  "Light snow showers"  : ["🌨️",  "🌨️"]}


# Get the data from YR helper function.
def get_xml_root():
    yr_response = 0
    try:
        yr_response = requests.get(yr_url)
        if yr_response.status_code != 200:
            print("Error: YR status code " + str(yr_response.status_code))
            exit()
        else:
            # We got a new response. Save it to the forecast file.
            with open(forecast_file, "w") as f:
                f.write(yr_response.text)
            # Return the data.
            return ET.fromstring(yr_response.text)
    except requests.ConnectionError:
        # Probably just no internet. Use latest forecast if there it is not to
        # old.
        if os.path.isfile(forecast_file):
            with open(forecast_file) as f:
                yr_response = f.read()
            return ET.fromstring(yr_response)
        else:
            print("No forecast data.")
            exit()


# Get forecast data from a forecast XML entry..
def parse_forecast(forecast):
    time_from =     forecast.attrib.get("from")
    time_to =       forecast.attrib.get("to")
    temp =          forecast.find("temperature").attrib.get("value")
    weather =       forecast.find("symbol").attrib.get("name")
    wind_dir =      forecast.find("windDirection").attrib.get("code")
    wind_speed =    forecast.find("windSpeed").attrib.get("mps")
    pressure =      forecast.find("pressure").attrib.get("value")
    precipitaion =  forecast.find("precipitation").attrib.get("value")
    return [time_from,  time_to,    temp,       weather, 
            wind_dir,   wind_speed, pressure,   precipitaion]
    

# Command line argument. Get desiered forecasts.
forecasts = 0
if len(sys.argv) == 2:
    forecasts = int(sys.argv[1])
else:
    print("Error, usage: \"" + sys.argv[0] + " <forecasts>\"")
    exit()


# Get the XML root.
xml_root = get_xml_root()

# Parse the location.
location = xml_root.find("location")
location_name = location.find("name").text
location_country = location.find("country").text

# Parse the sun rise and set time.
sun_rise_time = xml_root.find("sun").attrib.get("rise");
sun_rise_time = sun_rise_time[ sun_rise_time.find('T') + 1 : len(sun_rise_time) - 3 ]
sun_set_time = xml_root.find("sun").attrib.get("set");
sun_set_time = sun_set_time[ sun_set_time.find('T') + 1 : len(sun_set_time) - 3 ]

# Get todays weather.
if forecasts < 1:
    # No forecast. Exit.
    exit()

elif forecasts == 1:
    # One forecast. The user wants it on short form.
    forecast_now = xml_root.find("forecast").find("tabular").find("time")
    [time_from, time_to,    
     temp,      weather, 
     wind_dir,  wind_speed, 
     pressure,  precipitation] = parse_forecast(forecast_now);

    # Night time?
    sun_rise = datetime.datetime.strptime(sun_rise_time, "%H:%M")
    sun_set = datetime.datetime.strptime(sun_set_time, "%H:%M")
    now = datetime.datetime.now()
    night = 1 if now.time() < sun_rise.time() or sun_set.time() < now.time() else 0

    # Print the weather.
    if weather in weather_types:
        print(weather + ": " + weather_types.get(weather)[night] + " ", end="")
    else:
        print(weather + " ", end="")

    # Print the temperature and sun times.
    print(temp + "\u00B0", end=" ")
    print ("[" + sun_rise_time + " " + "🌅" + " " + sun_set_time + "]", end=" ")

    # Print the precipitation (if there is any).
    if precipitation != "0":
        # Print with a wet umbrella
        print("| ☔ " + precipitation + "mm", end=" ")

    # Print wind data.
    print("| 🍃 " + wind_speed + "m/s " + "(" + wind_dir + ")");

else: # forecasts > 1
    # Print weather meta data.
    print("Weather from YR.no for: " + location_name + ", " + location_country + ".")

    # More than one forecast. The user wants detailed data.
    forecast = xml_root.find("forecast")
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

