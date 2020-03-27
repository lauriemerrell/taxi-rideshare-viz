import pandas as pd
import numpy as np


#function assumes you will have columns from the city of Chicago data portal taxi or rideshare datasets
#generates a dataframe with day, hour, avg. of distance during that day/hour combination

def load_format_data_avg_distance(path):
    data = pd.read_csv(path)
    #convert trip start to datetime
    data['Trip Start Timestamp'] = pd.to_datetime(data['Trip Start Timestamp'], format = '%m/%d/%Y %I:%M:%S %p')
    
    #group by day, hour - get cumulative info (counts for rides and mean distance)
    times = pd.DatetimeIndex(data['Trip Start Timestamp'])
    data_by_day_hour = data.groupby([times.dayofweek, times.hour]).agg({'Trip ID': "count", 'Trip Miles': "mean"})
    data_by_day_hour.index.set_names(['day', 'hour'], inplace= True)
    data_by_day_hour.reset_index(inplace = True)
    
    #round -- default is too many decimals
    data_by_day_hour = data_by_day_hour.round(2)
    
    return data_by_day_hour


#load and reformat data - distance
taxi = load_format_data_avg_distance("Taxi_Trips.csv")
rideshare = load_format_data_avg_distance("Transportation_Network_Providers_-_Trips.csv")

#write reformatted data to file
taxi.to_csv("taxi_dist_by_day_hour.csv", index = False)
rideshare.to_csv("rideshare_dist_by_day_hour.csv", index = False)

