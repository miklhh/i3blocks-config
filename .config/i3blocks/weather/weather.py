#!/usr/bin/python3
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
                  "Light snow"          : ["🌨️",  "🌨️"],
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
            return ET.fromstring(yr_response.text)
    except requests.ConnectionError:
        # Probably just no internet. Use latest forecast.
        if os.path.isfile(forecast_file):
            with open(forecast_file) as f:
                yr_response = f.read()
            # Print recycle emoji and return.
            print("(♻️)", end=" ")
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
print(temp + "\u00B0C", end=" ")
print ("[" + sun_rise_time + " " + "🌅" + " " + sun_set_time + "]", end=" ")

# Print the precipitation (if there is any).
if precipitation != "0":
    # Print with a wet umbrella
    print("| ☔ " + precipitation + "mm", end=" ")

# Print wind data.
print("| 🍃 " + wind_speed + "m/s " + "(" + wind_dir + ")");
