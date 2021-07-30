from weatherforecast import closest_station
import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)
#fetch daily weather data from the closest station

r = requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/{}.dly'.format(closest_station))

weather = r.text

#save the weather data to a local file
with open('weather_{}.txt'.format(closest_station), "w") as weather_file:
    weather_file.write(weather)
