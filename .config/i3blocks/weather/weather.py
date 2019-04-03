#!/usr/bin/python3
import requests
import xml.etree.ElementTree as ET
import datetime
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

# Get the data from YR and handle caching.
def get_xml_root():
    yr_response = 0
    try:
        yr_response = requests.get(yr_url)
        if yr_response.status_code != 200:
            # Bad response code.
            print("Error: YR status code " + str(yr_response.status_code))
            exit()
        else:
            # We got a new response. Save it to the forecast file.
            with open(forecast_file, "w") as f:
                f.write(yr_response.text)
            return ET.fromstring(yr_response.text)
    except requests.ConnectionError:
        # Probably just no internet. Use cached forecast.
        if os.path.isfile(forecast_file):
            with open(forecast_file) as f:
                yr_response = f.read()
            # Print recycle emoji and continue using cached forecast.
            print("(♻️)", end=" ")
            return ET.fromstring(yr_response)
        else:
            # No internet and no cached forecast. This is a dead end.
            print("No forecast data.")
            exit()

# Get the XML root.
xml_root = get_xml_root()

# Parse the sun rise and set time. Appearntly, they are not always available and
# so we need to make sure they exist in the recieved data.
rise_fall_available = True
sun_rise_time = sun_set_time = ""
try:
    sun_rise_time = xml_root.find("sun").attrib.get("rise");
    sun_rise_time = sun_rise_time[ sun_rise_time.find('T') + 1 : len(sun_rise_time) - 3 ]
    sun_set_time  = xml_root.find("sun").attrib.get("set");
    sun_set_time  = sun_set_time[ sun_set_time.find('T') + 1 : len(sun_set_time) - 3 ]
except:
    rise_fall_available = False

# Get the current weather information.
forecast = xml_root.find("forecast").find("tabular").find("time")
weather = forecast.find("symbol").attrib.get("name")
temperature = forecast.find("temperature").attrib.get("value")
wind_direction = forecast.find("windDirection").attrib.get("code")
wind_speed = forecast.find("windSpeed").attrib.get("mps")
precipitation = forecast.find("precipitation").attrib.get("value")

# Night time?
night = 0
now = datetime.datetime.now()
if rise_fall_available:
    # Use sun rise and fall time to determine.
    sun_rise = datetime.datetime.strptime(sun_rise_time, "%H:%M")
    sun_set = datetime.datetime.strptime(sun_set_time, "%H:%M")
    night = 1 if now.time() < sun_rise.time() or sun_set.time() < now.time() else 0
else:
    # No rise/fall time available. Approximate daytime as [07:00 - 21:00]
    sun_rise = datetime.datetime.strptime("07:00", "%H:%M")
    sun_set = datetime.datetime.strptime("21:00", "%H:%M")
    night = 1 if now.time() < sun_rise.time() or sun_set.time() < now.time() else 0

# Print the weather.
if weather in weather_types:
    # Emoji avaiable for usage.
    print(weather + ": " + weather_types.get(weather)[night] + " ", end="")
else:
    # No emoji available, use regular text.
    print(weather + " ", end="")

# Print the temperature and sun times.
print(temperature, end="°C ")

# Print the sun rise and set time.
if rise_fall_available:
    print ("[" + sun_rise_time + " 🌅 " + sun_set_time + "]", end=" ")

# Print the precipitation (if there is any).
if precipitation != "0":
    # Print with a wet umbrella
    print("| ☔ " + precipitation + "mm", end=" ")

# Print wind data.
print("| 🍃 " + wind_speed + "m/s " + "(" + wind_direction + ")");
