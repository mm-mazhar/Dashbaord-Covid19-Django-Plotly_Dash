import warnings
warnings.filterwarnings("ignore")
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from dashboard.dash_apps.finished_apps.processDFs import covid_data, dict_of_locations


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('covidDashboard', external_stylesheets = external_stylesheets, meta_tags = [{"name": "viewport", "content": "width = device-width"}])

#third row
app.layout = html.Div([
    #first col
    html.Div([
        html.P("Select Country", style = {"color": "white"}),
        dcc.Dropdown(id = "w_countries",
                     multi = False,
                     searchable = True,
                     value = "US",
                     placeholder = "Select a country",
                     options = [{"label": i, "value": i}
                                for i in (covid_data["Country/Region"].unique())], style = {"background-color": "#545c63"}),
        
        html.P("New Cases: " + " " + str(covid_data["Date"].iloc[-1].strftime('%B %d, %Y')), 
                    className = "fix_label", style = {"text-align": "center", 'color': 'white', "padding-top": "30px"}),
        
        dcc.Graph(id = 'confirmed', config = {'displayModeBar': False}, style = {'margin-top': '30px'}),
                
        dcc.Graph(id = 'death', config = {'displayModeBar': False}, style = {'margin-top': '30px'}),
        
        dcc.Graph(id = 'recovered', config = {'displayModeBar': False}, style = {'margin-top': '30px'}),
        
        dcc.Graph(id = 'active', config = {'displayModeBar': False}, style = {'margin-top': '30px'})
        
    ], className = "three columns"),
    
    #Second col
    html.Div([
        #html.P("Pie Chart", style = {"color": "white"}),
        dcc.Graph(id = 'pie_chart', config = {'displayModeBar': 'hover'})
        
        ], className = "three columns"),
    
    #third col
    html.Div([
    dcc.Graph(id = 'line_chart', config = {'displayModeBar': 'hover'})
        ], className = 'six columns'),
    
    #map
    html.Div([
        dcc.Graph(id = 'map_chart', config = {'displayModeBar': 'hover'}
                      )
        ], className = 'twelve columns', style = {'margin-top': '50px'})
    
], className = "row")

#confirmed
@app.callback(Output('confirmed', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Confirmed'].iloc[-3]

    return {
        'data': [go.Indicator(
               mode = 'number+delta',
               value = value_confirmed,
               delta = {'reference': delta_confirmed,
                        'position': 'right',
                        'valueformat': 'g',
                        'relative': False,
                        'font': {'size': 10}},
               number = {'valueformat': ',',
                       'font': {'size': 15}},
               domain = {'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title = {'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'auto'}, #auto, top, bottom, middle
            font = dict(color = '#e1c027'),
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            height = 50,

        )
    }
#death    
@app.callback(Output('death', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Death'].iloc[-3]

    return {
        'data': [go.Indicator(
               mode = 'number+delta',
               value = value_death,
               delta = {'reference': delta_death,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 10}},
               number = {'valueformat': ',',
                       'font': {'size': 15}},
               domain = {'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title = {'text': 'New Death',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font = dict(color ='#d62635'),
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            height = 50,

        )
    }
#recovered
@app.callback(Output('recovered', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Recovered'].iloc[-3]

    return {
        'data': [go.Indicator(
               mode = 'number+delta',
               value = value_recovered,
               delta = {'reference': delta_recovered,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 10}},
               number = {'valueformat': ',',
                       'font': {'size': 15}},
               domain = {'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title = {'text': 'New Recovered',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font = dict(color = '#2e8657'),
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            height = 50,

        )
    }
#active
@app.callback(Output('active', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['Active'].iloc[-3]

    return {
        'data': [go.Indicator(
               mode = 'number+delta',
               value = value_active,
               delta = {'reference': delta_active,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 10}},
               number = {'valueformat': ',',
                       'font': {'size': 15}},
               domain = {'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title = {'text': 'New Active',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font = dict(color = '#e1c027'),
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            height = 50,

        )
    }
    
#Pie Chart    
@app.callback(Output('pie_chart', 'figure'), 
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Confirmed'].iloc[-1]
    death_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Death'].iloc[-1]
    recovered_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Recovered'].iloc[-1]
    active_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['Active'].iloc[-1]
    colors = ['#fcbf26', '#d62a42', '#2d8857', 'orange']

    return {
        'data': [go.Pie(
            labels = ['Confirmed', 'Death', 'Recovered', 'Active'],
            values = [confirmed_value, death_value, recovered_value, active_value],
            marker = dict(colors = colors),
            hoverinfo = 'label+value+percent',
            textinfo = 'label+value',
            hole = 0.5,
            rotation = 45,
            #insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title = {'text': 'Total Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color': 'white',
                       'size': 20},
            font = dict(family = 'sans-serif',
                      color = 'white',
                      size = 12),
            hovermode = 'closest',
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            legend = {'orientation': 'h',
                    'bgcolor': '#212529',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}


        )
    }

#Bar & Line Chart
@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_2 = covid_data.groupby(['Date', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'Date', 'Confirmed']].reset_index()
    covid_data_3['Daily Confirmed'] = covid_data_3['Confirmed'] - covid_data_3['Confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['Daily Confirmed'].rolling(window = 7).mean()


    return {
        'data': [go.Bar(
            x = covid_data_3['Date'].tail(30),
            y = covid_data_3['Daily Confirmed'].tail(30),
            name = 'Daily Confirmed Cases',
            marker = dict(color = '#fcbf26'),
            hoverinfo = 'text',
            hovertext = 
            '<b>Date</b>: ' + covid_data_3['Date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Daily Confirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'


        ),
            go.Scatter(
                x = covid_data_3['Date'].tail(30),
                y = covid_data_3['Rolling Ave.'].tail(30),
                mode = 'lines',
                name = 'Rolling Average of the last 7 days - daily confirmed cases',
                line = dict(width=3, color = '#FF00FF'),
                hoverinfo = 'text',
                hovertext = 
                '<b>Date</b>: ' + covid_data_3['Date'].tail(30).astype(str) + '<br>' +
                '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Rolling Ave.'].tail(30)] + '<br>'


            )],

        'layout': go.Layout(
            title = {'text': 'Last 30 Days Daily Confirmed Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color': 'white',
                       'size': 20},
            font = dict(family = 'sans-serif',
                      color = 'white',
                      size = 12),
            hovermode = 'closest',
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            legend = {'orientation': 'h',
                    'bgcolor': '#212529',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin = dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                       color = 'white',
                       showline = True,
                       showgrid = True,
                       showticklabels = True,
                       linecolor = 'white',
                       linewidth = 1,
                       ticks = 'outside',
                       tickfont = dict(
                           family = 'Aerial',
                           color = 'white',
                           size = 12
                       )),
            yaxis = dict(title = '<b>Daily Confirmed Cases</b>',
                       color = 'white',
                       showline = True,
                       showgrid = True,
                       showticklabels = True,
                       linecolor = 'white',
                       linewidth = 1,
                       ticks = 'outside',
                       tickfont = dict(
                           family = 'Aerial',
                           color = 'white',
                           size = 12
                       )
                       )
        )
    }

#map 
@app.callback(Output('map_chart', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_4 = covid_data.groupby(['Lat', 'Long', 'Country/Region'])[['Confirmed', 'Death', 'Recovered', 'Active']].max().reset_index()
    covid_data_5 = covid_data_4[covid_data_4['Country/Region'] == w_countries]

    if w_countries:
        zoom = 2
        zoom_lat = dict_of_locations[w_countries]['Lat']
        zoom_long = dict_of_locations[w_countries]['Long']



    return {
        'data': [go.Scattermapbox(
            lon = covid_data_5['Long'],
            lat = covid_data_5['Lat'],
            mode = 'markers',
            marker = go.scattermapbox.Marker(size = covid_data_5['Confirmed'] / 1500,
                                           color = covid_data_5['Confirmed'],
                                           colorscale = 'HSV',
                                           showscale = False,
                                           sizemode = 'area', #diameter #area
                                           opacity = 0.3),
            hoverinfo = 'text',
            hovertext = 
            '<b>Country</b>: ' + covid_data_5['Country/Region'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + covid_data_5['Long'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + covid_data_5['Lat'].astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['Confirmed']] + '<br>' +
            '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_5['Death']] + '<br>' +
            '<b>Recovered Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['Recovered']] + '<br>' +
            '<b>Active Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['Active']] + '<br>'


        )],

        'layout': go.Layout(
            hovermode = 'x',
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            margin = dict(r = 0, l = 0, b = 0, t = 0),
            mapbox = dict(
                accesstoken = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center = go.layout.mapbox.Center(lat = zoom_lat, lon = zoom_long),
                style = 'dark',
                zoom = zoom,
            ),
            autosize = True



        )
    }