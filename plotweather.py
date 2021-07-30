import sqlite3
import pandas as pd


conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

# retrieve the maximum temperature data 
# from the weather database  

cursor.execute("""SELECT * FROM weather
                  WHERE element in ('TMAX', 'TMIN')
                  ORDER BY year, month""")

tmax_tmin_data = cursor.fetchall()
print(tmax_tmin_data[0])

tmax_data = [x for x in tmax_tmin_data if x[3] == 'TMAX']
tmin_data = [x for x in tmax_tmin_data if x[3] == 'TMIN']

#print(tmin_data[:5])

#plotting

tmax_df = pd.DataFrame(tmax_data, columns=['Station', 'Year', 'Month',
                                           'Element', 'Max', 'Min',
                                           'Mean', 'Days'])

tmin_df = pd.DataFrame(tmin_data, columns=['Station', 'Year', 'Month',
                                           'Element', 'Max', 'Min',
                                           'Mean', 'Days'])




tmax_tmin_avg_by_year = tmin_df[['Year', 'Min', 'Max', 'Mean']].groupby('Year').mean()

ax = tmax_tmin_avg_by_year.plot(figsize=(16,4), title="Maximum and Minimum Temperature in 100 years")

ax.figure.savefig('tmax_tmin_tavg_by_year.png')
