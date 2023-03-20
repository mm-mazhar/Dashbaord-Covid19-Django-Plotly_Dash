import warnings
warnings.filterwarnings("ignore")
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import io
import requests
from django_plotly_dash import DjangoDash


url3 = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-age-group.csv"
s3 = requests.get(url3).content
dfByAge = pd.read_csv(io.StringIO(s3.decode('utf-8')))
df3copy = dfByAge.copy()
df3copy.sort_values(by = ['date', 'location'], inplace = True)

#Fill NaN with 0
df3copy.fillna(0, inplace = True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('vaccinesByAge', external_stylesheets = external_stylesheets, meta_tags = [{"name": "viewport", "content": "width = device-width"}])


app.layout = html.Div([
    
    html.Div([
        html.H6("Vaccination By Age", style = {"color": "white", "margin-top": "5px"}),
        html.P("Select Country", style = {"color": "white"}),
        
        dcc.Dropdown(id = "w_countries",
                     multi = False,
                     searchable = True,
                     value = "Iceland",
                     placeholder = "Select or Type Country Name",
                     options = [{"label": i, "value": i}
                                for i in (df3copy["location"].unique())], style = {"width": "50%",
                                                                              #"background-color": "#545c63",
                                                                              }),
        
        dcc.Graph(id = 'vacc_age_country', config = {'displayModeBar': True}, style = {'margin-top': '5px'}),
        ], 
        className = "twelve columns"),
    
], className = "row")

#vacc_age_country
@app.callback(Output('vacc_age_country', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    df3 = df3copy.copy()
    df3 = df3[df3['location'] == w_countries]
    
    fig = px.line(df3,
                  x = 'date',
                  y = 'people_fully_vaccinated_per_hundred',
                  color = 'age_group',
                  hover_data = ['location', 'age_group', 'people_fully_vaccinated_per_hundred'],
                  #color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
                  #color_discrete_sequence = px.colors.diverging.Phase,
                  labels = {'date': 'Date', 'people_fully_vaccinated_per_hundred': 'Fully Vaccinated People Per Hundred'},
                  height = 400,
            )
    
    fig.update_layout({
    'plot_bgcolor': '#212529',
    'paper_bgcolor': '#212529',
    'xaxis': {'gridcolor': '#212529'},
    'yaxis': {'gridcolor': '#212529'},
    'xaxis': {'color': 'white'},
    'yaxis': {'color': 'white'},
    'legend': {'font': {'color': 'white'}, 'title': 'Vaccine'},
    })
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
        
    return fig