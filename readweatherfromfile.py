with open('weather_CA007014290.txt', 'r') as weather_file:
    weather = weather_file.read()



def parse_line(line):
    """parses the lines of the weather data
        and eliminates missing values (-9999C)"""

    #return None if line is empty
    if not line:
        return None

    #split the first 4 fields and string containing
    #temperature values:

    record, temperature_string = (line[:11], int(line[11:15]),
                                  int(line[15:17]), line[17:21]), line[21:]

    if len(temperature_string) < 248:
        raise ValueError(f"String not long enough - \
                            {temperature_string} {str(line)}")

    #convert the temperature_strings into floats
    #and filter the data that's missing (-9999)

    values = [float(temperature_string[i:i + 5])/10 \
              for i \
              in range (0,248,8) \
              if not temperature_string[i:i + 5].startswith("-9999")]

    #compute summary statistics on the temperature data
    count = len(values)
    tmax = round(max(values), 1)
    tmin = round(min(values), 1)
    mean = round(sum(values) / count, 1)

    #add the metadata to the summary statistics

    return record + (tmax, tmin, mean, count)

#check if it works on one record:

print(parse_line(weather[:270]))

#process all the weather data
weather_data = [parse_line(x) for x in weather.split("\n") if x]

print(weather_data)


