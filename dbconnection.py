#creates a database to hold the weather data
#from the closest weather station
import sqlite3

from readweatherfromfile import weather_data

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

#create weather table:

create_weather = """CREATE TABLE "weather" (
                        "id" text NOT NULL,
                        "year" integer NOT NULL,
                        "month" integer NOT NULL,
                        "element" text NOT NULL,
                        "max" real,
                        "min" real,
                        "mean" real,
                        "count" integer)"""

cursor.execute(create_weather)
conn.commit()

# store the data into the newly created db

for field in weather_data:
    cursor.execute("""INSERT INTO weather (id, year,
                   month, element, max, min,
                   mean, count) VALUES (?, ?, ?, ?, ?,
                   ?, ?, ?) """, field)
conn.commit()

print('db created!')




