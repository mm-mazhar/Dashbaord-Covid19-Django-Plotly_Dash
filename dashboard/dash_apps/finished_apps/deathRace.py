# https://plotly.com/python/animations/
# https://towardsdatascience.com/how-to-produce-an-animated-bar-plot-in-plotly-using-python-2b5b360492f8

import warnings
warnings.filterwarnings("ignore", category = FutureWarning)
import pandas as pd    
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dashboard.dash_apps.finished_apps.processDFs import dfd, month_yearD, dict_keysD

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('animationDeathGraph', external_stylesheets = external_stylesheets, meta_tags=[{"name": "viewport", "content": "width = device-width"}])
#-------------------------------------------
# Data Fetching and Preparation

# print("\n")
# print("dfd: \n",dfd)

# print("\n")
# print("month_yearD: \n",month_yearD)

# print("\n")
# print("Dict Keys: \n", dict_keysD)

n_frame={}

for y, d in zip(month_yearD, dict_keysD):
    
    try:
        if dfd['MonthYear'].loc[dfd['MonthYear'] == y].unique().tolist()[0] == y:
            dataframe = dfd[(dfd['MonthYear'] == y)]
            dataframe = dataframe.nlargest(n = 10, columns = ['death'])
            #dataframe = dataframe.sort_values(by = ['MonthYear','death'])
            n_frame[d] = dataframe
            
    except Exception as e:
        pass

# print (n_frame)

#-------------------------------------------
# Create Animated Bar Chart and store figure as fig
fig = go.Figure(
    data = [
        go.Bar(
        x = n_frame[dict_keysD[0]]['death'],
        y = n_frame[dict_keysD[0]]['Country/Region'],
        orientation = 'h',
        text = n_frame[dict_keysD[0]]['death'],
        texttemplate = '%{text:.3s}',
        textfont = {'size': 18},
        textposition = 'inside',
        insidetextanchor = 'middle',
        width = 0.7,
        #marker = {'color': '#000'},
        marker = {'color': n_frame[dict_keysD[0]]['color_code']}
        )
    ],
    layout = go.Layout(
        xaxis = dict(range = [1000, 1000000], autorange = False, 
                    tickfont = dict(size = 14, color = '#545c63'),
                    title = dict(text = 'Deaths', font = dict(size = 18, color = '#FFF')),
                    showgrid = False, 
                    #gridwidth = 1,
                    #gridcolor = '#545c63',
                    tickangle = 45,
                    ),
        yaxis = dict(range = [-0.5, 11.5], #[-0.5, 5.5],
                     autorange = False,
                     tickfont = dict(size = 14, color = '#545c63'),
                     #tickangle = 315,
                     ),
        title = dict(text = 'Deaths till: ' + str(pd.to_datetime(dict_keysD[0], format = '%m-%Y').strftime('%B %Y')),
                     font = dict(size = 28, color = '#FFF'),
                     x = 0.5,
                     xanchor = 'center'),
        paper_bgcolor = '#212529',
        plot_bgcolor = '#212529',
        
        #width = 500, #also adjust width, height, ratio in deathRace.html
        #height = 500,
        #margin = dict(l = 50, r = 50, b = 100, t = 100, pad = 4),
        
        #hovermode = "closest",
        
        # Add button
        # https://plotly.com/python/animations/
        # https://towardsdatascience.com/how-to-produce-an-animated-bar-plot-in-plotly-using-python-2b5b360492f8
        updatemenus = [dict(
            type = "buttons",
            buttons = [dict(label = "Play",
                          method = "animate",
                          # https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
                          args = [None,
                          {"frame": {"duration": 500, "redraw": True},
                           "fromcurrent": True,
                          "transition": {"duration": 250,
                          "easing": "linear"}}]
                            ),
                    #stop button
                       dict(label = "Stop",
                            method = "animate",
                            args = [None,
                          {"frame": {"duration": 0, "redraw": False},
                           "mode": "immediate",
                          "transition": {"duration": 0,
                          "easing": "linear",
                                        }}]
                            )
                    ], 
            direction = "left",
            pad = {"l": 30, "t": 10},
            #show_active = True,
            #x=0.0,
            #xanchor = "right",
            #y=1.1,
            #yanchor = "top"
        )]
    ),
    frames = [
            go.Frame(
                data = [
                        go.Bar(x = value['death'], 
                                y = value['Country/Region'],
                                orientation = 'h',
                                text = value['death'],
                                #marker = {'color': '#000'},
                                marker = {'color': value['color_code']}
                        )
                    ],
                layout = go.Layout(
                        xaxis = dict(range=[1000, 1000000], autorange = False),
                        yaxis = dict(range = [-0.5, 11.5], autorange = False, #[-0.5, 5.5],
                                     tickfont = dict(size = 14)),
                        title = dict(text = 'Deaths Per Country till: ' + str(pd.to_datetime(value['MonthYear'].values[0], format = '%m-%Y').strftime('%B %Y')),
                        #title = dict(text = 'Deaths Per Country: ' + str(value['MonthYear'].values[0]),
                        font = dict(size = 28),
                        ),
                    )
            )
        for key, value in n_frame.items()
    ]
)

#-------------------------------------------
app.layout = html.Div(children = [
    dcc.Graph(
        id = 'animatedDeaths-graph',
        figure = fig,
        #style = {'height': '500px'}
        
    )
])

