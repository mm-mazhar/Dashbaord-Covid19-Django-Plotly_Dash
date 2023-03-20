import warnings
warnings.filterwarnings("ignore")
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import io
import requests
from django_plotly_dash import DjangoDash

noDays = 90
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))
dfcopy = df.copy()
noDays = dfcopy['date'].nunique()
#df.isnull().sum()
#Fill NaNs with 0 and then drop all countries with iso_code = 0. This is key information that we need so dropping unknowns is the best way to handle. 
dfcopy.fillna(0, inplace = True)
dfcopy.drop(dfcopy.index[dfcopy['iso_code'] == 0], inplace = True)
dfcopy.drop(dfcopy.index[dfcopy['total_vaccinations'] == 0], inplace = True)
#Check how many nulls we have. SHould be none. 
#df.isnull().sum()
#df.info()
#The date is in the 'object' format. Let us change it to Datetime format for easy handling and plotting. 
dfcopy['date'] =  pd.to_datetime(dfcopy['date'], format = '%Y-%m-%d')
#Print column names and drop the ones we don't intend to use. 
#print(df.columns)
dfcopy.drop(['iso_code','total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 
         'total_boosters', 'daily_vaccinations_raw', 'daily_vaccinations',
         'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
         "daily_vaccinations_raw", "daily_vaccinations_per_million", 
         'total_boosters_per_hundred', 'daily_vaccinations_per_million',
         'daily_people_vaccinated_per_hundred',
         ], axis = 1, inplace = True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('vaccinesAnalysis', external_stylesheets = external_stylesheets, meta_tags=[{"name": "viewport", "content": "width = device-width"}])


app.layout = html.Div([
    #1st item
    html.Div([
        html.H6("Daily Vaccination", style = {"color": "white", "margin-top": "5px"}),
        html.P("Change Country", style = {"color": "white"}),
        
        dcc.Dropdown(id = "w_countries",
                     multi = False,
                     searchable = True,
                     value = "United States",
                     placeholder = "Select or Type Country Name",
                     options = [{"label": i, "value": i}
                                for i in (dfcopy["location"].unique())], style = {'width': "50%",
                                                                              #"background-color": "#545c63",
                                                                              }),
        
        dcc.Graph(id = 'daily_people_vaccinated', config = {'displayModeBar': True}, style = {'margin-top': '5px'}),
        ], 
        className = "six columns"),
    
    #2nd item
    html.Div([
        html.H6("Fully Vaccinated People Per Hundered", style = {"color": "white", "margin-top": "5px",}),
        dcc.Graph(id = 'fully_vaccinated_per_hundered', config = {'displayModeBar': True}, style = {'margin-top': '80px'}),
        ], 
        className = "six columns"),
    
], className = "row")

#daily_people_vaccinated
@app.callback(Output('daily_people_vaccinated', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    
    df1 = dfcopy[dfcopy['location'] == w_countries][['location', 'date', 'daily_people_vaccinated']].reset_index()
    df1['Rolling Ave.'] = df1['daily_people_vaccinated'].rolling(window = 7).mean()

    return {
        'data': [go.Bar(
            x = df1['date'].tail(noDays),
            y = df1['daily_people_vaccinated'].tail(noDays),
            name = 'Daily People Vaccinated',
            marker = dict(color = '#fcbf26'),
            hoverinfo = 'text',
            hovertext = 
            '<b>Date</b>: ' + df1['date'].tail(noDays).astype(str) + '<br>' +
            '<b>People Vaccinated Today</b>: ' + [f'{x:,.0f}' for x in df1['daily_people_vaccinated'].tail(noDays)] + '<br>' +
            '<b>Country</b>: ' + df1['location'].tail(noDays).astype(str) + '<br>'


        ),
            go.Scatter(
                x = df1['date'].tail(noDays),
                y = df1['Rolling Ave.'].tail(noDays),
                mode = 'lines',
                name = 'Rolling Average of the last 7 days',
                line = dict(width = 3, color = '#FF00FF'),
                hoverinfo = 'text',
                hovertext = 
                '<b>Date</b>: ' + df1['date'].tail(noDays).astype(str) + '<br>' +
                '<b>MV Today</b>: ' + [f'{x:,.0f}' for x in df1['Rolling Ave.'].tail(noDays)] + '<br>'


            )],

        'layout': go.Layout(
            title = {'text': 'People Vaccinated in ' + (w_countries) + ' in Last ' + str(noDays) + ' Days',
                   'y': 0.9,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color': 'white',
                       'size': 15},
            font = dict(family = 'sans-serif',
                      color = 'white',
                      size = 12),
            hovermode = 'closest',
            paper_bgcolor = '#212529',
            plot_bgcolor = '#212529',
            legend = {'orientation': 'h',
                    'bgcolor': '#212529',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.5},
            margin = dict(r = 0),
            xaxis = dict(title = '<b>Date</b>',
                       color = 'white',
                       showline = True,
                       showgrid = False,
                       showticklabels = True,
                       linecolor = 'white',
                       linewidth = 1,
                       ticks = 'outside',
                       tickangle = 315,
                       tickfont = dict(
                           family = 'Aerial',
                           color = 'white',
                           size = 12,
                           )),
            yaxis = dict(title = '<b>Daily People Vaccinated</b>',
                       color = 'white',
                       showline = True,
                       showgrid = False,
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
    
#fully_vaccinated_per_hundered
@app.callback(Output('fully_vaccinated_per_hundered', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    df2 = dfcopy[dfcopy['location'] == w_countries][['location', 'date', 'people_fully_vaccinated_per_hundred']].reset_index()
    
    fig = px.line(df2,
                  x = 'date',
                  y = 'people_fully_vaccinated_per_hundred',
                  color = 'location',
                  hover_data = ['location', 'date', 'people_fully_vaccinated_per_hundred'],
                  #color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
                  #color_discrete_sequence = px.colors.diverging.Phase,
                  labels = {'date': 'Date', 'people_fully_vaccinated_per_hundred': 'Fully Vaccinated People Per Hundred'},
                  height = 450,
                  title = "Fully Vaccinated People Per Hundred in " + (w_countries),
                  #legend_title = 'Country',
            )
    
    fig.update_layout({
    'plot_bgcolor': '#212529',
    'paper_bgcolor': '#212529',
    'xaxis': {'gridcolor': '#212529'},
    'yaxis': {'gridcolor': '#212529'},
    'xaxis': {'color': 'white'},
    'yaxis': {'color': 'white'},
    'legend': {'font': {'color': 'white'}, 'title': 'Country'},
    'title': {'x': 0.5, 'y': 0.9, 'xanchor': 'center', 'yanchor': 'top', 'font': {'color': 'white', 'size': 15}},
    })
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
        
    return fig