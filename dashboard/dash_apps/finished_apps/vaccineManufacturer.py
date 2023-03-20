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


url2 = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv"
s2 = requests.get(url2).content
df2 = pd.read_csv(io.StringIO(s2.decode('utf-8')))
df2copy = df2.copy()

#Fill NaN with 0
df2copy.fillna(0, inplace = True)
df2copy.drop(df2copy[df2copy['location'] == 'European Union'].index, inplace = True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('vaccinesByManufacturer', external_stylesheets = external_stylesheets, meta_tags = [{"name": "viewport", "content": "width = device-width"}])


app.layout = html.Div([
    
    html.Div([
        html.H6("Countries with Doses Administered by Manufacturers", style = {"color": "white", "margin-top": "5px"}),
        html.P("Select Country", style = {"color": "white"}),
        
        dcc.Dropdown(id = "w_countries",
                     multi = False,
                     searchable = True,
                     value = "United States",
                     placeholder = "Select or Type Country Name",
                     options = [{"label": i, "value": i}
                                for i in (df2copy["location"].unique())], style = {'width': "50%"}),
        
        dcc.Graph(id = 'vacc_manuf_country', config = {'displayModeBar': True}, style = {'margin-top': '5px'}),
        ], 
        className = "twelve columns"),
    
], className = "row")

#vacc_manuf_country
@app.callback(Output('vacc_manuf_country', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    df2 = df2copy.copy()
    lastDate = df2[df2['location'] == w_countries]['date'][-1:].iloc[0]
    df2 = df2[(df2['location'] == w_countries) & (df2['date'] == lastDate)]

    fig = px.bar(df2,
            x = 'location',
            y = 'total_vaccinations',
            color = 'vaccine',
            hover_data = ['location', 'vaccine', 'total_vaccinations'],
            color_discrete_map = {
                "Moderna": "goldenrod",
                "Oxford/AstraZeneca": "green",
                "Sinopharm/Beijing": "#e94e3a",
                "Sputnik V": "#3acd99",
                "Pfizer/BioNTech": "#414a8f",
                "CanSino": "#0d0887",
                "Johnson&Johnson": "blue",
                "Novavax": "magenta",
                "Sinovac": "#a663f6",
                "Covaxin": "#7201a8",
                },
            #color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
            #color_discrete_sequence = px.colors.diverging.Phase,
            barmode = 'group',
            labels = {'location': 'Country', 'total_vaccinations': 'Total Vaccinations'},
            height = 400,
            )

    #fig.update_layout(xaxis = {'categoryorder':'total ascending'})
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