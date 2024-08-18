################################################ NEW YORK CITIBIKE DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='New York CitiBike Strategy Dashboard', layout='wide')
st.title("New York CitiBike Strategy Dashboard")

## Define Side Bar
page = st.sidebar.selectbox('Select an aspect of the analysis',
                            ['Intro page',
                             'Weather Component and Bike Usage',
                             'Most Popular Stations',
                             'Interactive Map with Aggregated Bike Trips',
                             'Recommendations'])

st.markdown("The dashboard will help with the expansion problems CitiBike currently faces")
st.markdown("The increase in popularity of bike sharing has led to distribution problems for CitiBike. As there are fewer bikes at popular bike stations or stations full of docked bikes, making it difficult to return a hired bike and increase in customer complaints.")

########################## IMPORT DATA ###########################################################################################

df = pd.read_csv('nycbike_sample_dashboard.csv', index_col=0)
df_date = pd.read_csv('NYCitiBike_trip_temp.csv', index_col = 0)
top20_data = pd.read_csv('top20_station.csv', index_col=0)

# ######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("#### The dashboard will help with the expansion problems CitiBike currently faces.")
    st.markdown("The increase in popularity of bike sharing has led to distribution problems for CitiBike. As there are fewer bikes at popular bike stations or stations full of docked bikes, making it difficult to return a hired bike and increase in customer complaints. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most Popular Stations")
    st.markdown("- Weather Component and Bike Usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")


### Dual axis line chart page ###
    
elif page == 'Weather Component and Bike Usage':

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(x=df_date['date'], y=df_date['trips_per_day'], name='Daily Count of Bike Rides',
                   marker={'color': 'green'}),
        secondary_y=False)

    fig_2.add_trace(
        go.Scatter(x=df_date['date'], y=df_date['avgTemp'], name='Daily Average Temperature',
                   marker={'color': 'blue'}),
        secondary_y=True)

    fig_2.update_layout(
        title='Bike Rides and Temperature Over Time',
        xaxis_title='Date',
        yaxis_title='Count of Bike Rides',
        yaxis2_title='Average Temperature (°C)',
        height=600
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("The chart indicates that bike usage peaks from May to October, aligning with warmer months. During this period, there is a noticeable increase in daily bike rides, which correlates with higher average temperatures. Conversely, bike usage drops as temperatures decrease, particularly during the colder months from November to April. This trend highlights how temperature plays a significant role in influencing biking activity throughout the year.")

### Most popular stations bar chart page ###

elif page == 'Most Popular Stations':
    
    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label='Select the season', options=df['season'].unique(),
                                       default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['trips_per_day'].count())
    st.metric(label='Total Bike Rides', value=numerize(total_rides))

    # Bar chart
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    
    fig = go.Figure(go.Bar(x=top20['start_station_name'], y=top20['value'], 
                           marker={'color': top20['value'], 'colorscale': 'blugrn'}))
    
    fig.update_layout(
        title='Top 20 of the Most Popular Bike Stations in New York',
        xaxis_title='Start Stations Name',
        yaxis_title='Total Count of Trips',
        width=900, height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The bar chart highlights the most popular bike stations in New York, with W 21 St & 6 Ave emerging as the top station, followed closely by West St & Chambers St and Broadway & W 58 St. The significant drop from the highest to the lowest counts in the chart suggests that these top stations are clear favorites among users. This insight can be valuable when considering station expansions or bike availability strategies, as it identifies key areas of high demand that might require more resources to meet user needs.")

### Map Page ###

elif page == 'Interactive Map with Aggregated Bike Trips': 

    ### Create the map ###
    st.write("Interactive map showing aggregated bike trips over NYC")

    path_to_html = "NY_CitiBike_popular.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in NYC")
    st.components.v1.html(html_data, height=1000)
    st.markdown("Based on the map, we can see that a lot of customers from CitiBike are using their services around the Central Park areas and along road near the Hudson River.")
    st.markdown("While having the aggregated bike trips filter enabled, we can see that even though W 21 St & 6 Ave is a popular start station, it doesn't account for the most commonly taken trips. Instead, the Central Park S & 6 Ave is more commonly taken trips.")


### Conclusion page ###

else:
    
    st.header("Conclusions and Recommendations")
    
    st.markdown("### Our analysis has shown that CitiBike should focus on the following objectives moving forward:")
    st.markdown("- Given the high concentration of trips near Central Park and along the Hudson River, it would be beneficial to increase bike availability in these areas, especially during peak seasons. This redistribution could help alleviate shortages in high-demand locations and ensure a more balanced distribution across the city.")
    st.markdown("- Consider expanding the available bike stations to areas adjacent to Central Park and the Hudson River, where trips are most commonly taken. This strategy could improve accessibility for users who prefer these popular routes, thereby enhancing overall user satisfaction.")
    st.markdown("- The business strategy team should consider implementing a seasonal bike distribution model, where more bikes are allocated to popular stations during warmer months. This approach would help address the increased demand during the peak biking season and ensure availability across all stations.")
    st.markdown("- Consider conducting further analysis on the demographics of the customers such as their age and gender or whether they are tourists or local customers. This would help to develop more tailored marketing campaigns or memberships based on CitiBike's customers.")
