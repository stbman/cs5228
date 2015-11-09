import plotly.plotly as py
import pandas as pd

df_airports = pd.read_csv('latlong.csv')
df_airports.head()

df_flight_paths = pd.read_csv('pairdistances.latlong.csv', nrows=1000)
df_flight_paths.head()

airports = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_airports['Longtitude'],
        lat = df_airports['Latitude'],
        hoverinfo = 'text',
        text = df_airports['Port'],
        mode = 'markers',
        marker = dict(
            size=2,
            color='rgb(255, 0, 0)',
            line = dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

flight_paths = []
for i in range( len( df_flight_paths ) ):
    flight_paths.append(
        dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = [ df_flight_paths['Origin_long'][i], df_flight_paths['Dest_long'][i] ],
            lat = [ df_flight_paths['Origin_lat'][i], df_flight_paths['Dest_lat'][i] ],
            mode = 'lines',
            line = dict(
                width = 1,
                color = 'red',
            ),
            #opacity = float(df_flight_paths['cnt'][i])/float(df_flight_paths['cnt'].max()),
        )
    )

layout = dict(
        title = '2007 American Airline flight paths',
        showlegend = False,
        geo = dict(
            scope='north america',
            projection=dict( type='azimuthal equal area' ),
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )

fig = dict( data=flight_paths + airports, layout=layout )
url = py.plot( fig, filename='d3-flight-paths' )
