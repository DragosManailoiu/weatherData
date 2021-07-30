import requests
from collections import namedtuple
import pprint
import math

pp = pprint.PrettyPrinter(indent=2)

r = requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt')
readme = r.text


#fetch the inventory and the stations files
r = requests.get("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt")
inventory_txt = r.text

r = requests.get("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
stations_txt = r.text

# save the two files on disk

with open("inventory.txt", "w") as inventory_file :
    inventory_file.write(inventory_txt)

with open("stations.txt", "w") as stations_file:
    stations_file.write(stations_txt)

#print(inventory_txt)

#creates an inventory class using named tuples
Inventory = namedtuple("Inventory", ['station', 'latitude', 'longitude',
                        'element', 'start', 'end'])

#parse the rows of the inventory file and give them the inventory type
#cast the latitude and longitude to float type
#cast the start and end date to int type
inventory = [Inventory(x[0:11], float(x[12:20]), float(x[21:30]), x[31:35],
                       int(x[36:40]), int(x[41:45]))
             for x in inventory_txt.split("\n") if x.startswith("CA")]

#filter the data on the elements TMIN and TMAX
#to retrieve the temperature data
#we want at least 90 years of data

inventory_temp = [x for x in inventory if x.element in ["TMIN", "TMAX"]
                  and x.start < 1920 and x.end >= 2010]


#we're interested in the stations near me

#montreal's coordinates on the map:
mtl_latitude, mtl_longitude = 45.5089, -73.5617

#sort the inventories based on how close they are from us
#use the eucledian distance formula to calculate the distance

inventory_temp.sort(key=lambda x: math.sqrt((abs(mtl_latitude - x.latitude))**2 + (abs(mtl_longitude - x.longitude))**2))

#retrieve the 5 closest weather station

closest_station = inventory_temp[0].station
print(closest_station)


#station metadata
"""------------------------------
Variable   Columns   Type
------------------------------
ID            1-11   Character
LATITUDE     13-20   Real
LONGITUDE    22-30   Real
ELEVATION    32-37   Real
STATE        39-40   Character
NAME         42-71   Character
GSN FLAG     73-75   Character
HCN/CRN FLAG 77-79   Character
WMO ID       81-85   Character
------------------------------"""

#look for matcches in the start and end year 

Station = namedtuple("Station", ['station_id', 'latitude', 'longitude',
                                    'elevation', 'state', 'name', 'start', 'end'])

stations = [(x[0:11], float(x[12:20]), float(x[21:30]), float(x[31:37]),
             x[38:40].strip(), x[41: 71].strip())
            for x in stations_txt.split("\n") if x.startswith(closest_station)]

#create a station object
station = Station(*stations[0] + (inventory_temp[0].start,
     inventory_temp[0].end))

print(station)

#station "les cedres" - QC is the closest weather station from my place"

