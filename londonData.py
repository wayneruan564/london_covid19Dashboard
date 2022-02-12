import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px #if using plotly
import geopandas as gpd
import os
import numpy as np
import pyproj

from plotly.graph_objects import Layout
import plotly.graph_objects as go



#getting weekly data, separated by boroughs.

#daily covid case
df_cases = pd.read_csv('https://data.london.gov.uk/download/coronavirus--covid-19--cases/151e497c-a16e-414e-9e03-9e428f555ae9/phe_cases_london_boroughs.csv')
df_cases = df_cases.drop(columns= ['area_code', 'total_cases'])

#daily covid death case
df_death = pd.read_csv('https://data.london.gov.uk/download/coronavirus--covid-19--cases/ff60cf44-852e-425e-960c-869920dcdd0d/phe_deaths_london_boroughs.csv')

#hospital admissions
hospitalAdmission = pd.read_csv('https://data.london.gov.uk/download/coronavirus--covid-19--cases/ad037e43-0f09-473a-8d62-b576de380af6/phe_healthcare_admissions_age.csv')

population = pd.read_csv('london_population_2020.csv')



# reading in the London shapefile
fp = "London_Borough_Excluding_MHW.shp"
map_df = gpd.read_file(fp)
# map_df = map_df[['NAME', 'geometry']]
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
map_df = map_df.rename(columns={"NAME": "area_name"})
map_df = map_df.drop(columns = ['HECTARES', 'NONLD_AREA', 'ONS_INNER', 'SUB_2009', 'SUB_2006'])

#using the coordinates, we can label each region by its GSS_CODE on the map.
map_df['coords'] = map_df['geometry'].apply(lambda x: x.representative_point().coords[:])
map_df['coords'] = [coords[0] for coords in map_df['coords']]






#merge covid death data and covid cases together.
df_daily = df_cases.merge(df_death, on=["date", "area_name"])
df_daily = df_daily.drop(columns= ['total_deaths'])

#pivot covid case dataframe for plotting purpose
df_pivoted = df_cases.pivot_table(values='new_cases', index=df_cases.area_name, columns='date')


#for geo map case per 100,000 people
df_modified = df_pivoted.T.reset_index()
df_modified = df_modified.assign(Weeks = df_modified['date']).drop(columns='date')
df_modified['Weeks'] = df_modified['Weeks'].astype('datetime64[ns]')
weekly_case = df_modified.resample('W-Mon', label='left', closed='left', on='Weeks').sum()
weekly_case.index = weekly_case.index.astype(str)

#transpose for plotting purpose
weekly_case = weekly_case.T

#merge geodataframe and region data together.
df_merged = weekly_case.merge(population, on="area_name")
df_merged.set_index("area_name", inplace = True)



#weekly covid case per 100,000 people.
d = df_merged['ONS']
result = df_merged.div(d, axis=-0)
result = result.drop(columns= ['ONS', 'GLA', 'Difference'])
result = round(result * 100000)

#combine our geodataframe and weekly case data together, so we can plot data in respective regions.
df_merged1 = map_df.merge(result, on="area_name")
df_merged1.index = df_merged1['area_name']



#retrieving the most recent weekly data on hospital admissions
hospitalAdmissionRecent = hospitalAdmission.sort_values(by="week_ending").tail(5).sort_values(by="age")




#group regions by day. This is used to plot the daily covid case.
df_grouped = df_cases.groupby(by=['date']).sum()
df_grouped

#setting up x and y variable for plotting daily Case line chart.
x = df_grouped.index
y = df_grouped['new_cases']




#get the last 14 days' covid daily cases data.
df_lastTwoWeeks = df_grouped.tail(14)
df_lastTwoWeeks

#for plotting bar chart for the last 14 days.
x1 = df_lastTwoWeeks.index
y1 = df_lastTwoWeeks['new_cases']


