import dash_table
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dashboard.dash_apps.finished_apps.processDFs import covid_data
from dashboard.dash_apps.finished_apps.vaccinesAnalysis import dfcopy
from dashboard.dash_apps.finished_apps.vaccineManufacturer import df2copy
from dashboard.dash_apps.finished_apps.vaccinations_by_age_group import df3copy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('dtables', external_stylesheets = external_stylesheets, meta_tags = [{"name": "viewport", "content": "width = device-width"}])

#---------------------------------------------------------------
# Data Table import from 
dff = covid_data.copy()
dff2 = dfcopy.copy()
dff3 = df2copy.copy()
dff3.drop(dff3[dff3['location'] == 'European Union'].index, inplace = True)
dff4 = df3copy.copy()
#---------------------------------------------------------------
app.layout = html.Div([
    
    html.Div([
        html.H6('JHU CSSE COVID-19 Dataset', style = {"color": "white"}),
        html.P("Three time series tables are for the global confirmed cases, recovered cases, active and deaths combined", style = {"color": "white"}),
        dcc.Link(html.A('Data Source: CSSE at Johns Hopkins University'), href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('time_series_covid19_confirmed_global.csv'), href="https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('time_series_covid19_deaths_global.csv'), href="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('time_series_covid19_recovered_global.csv'), href="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", style={'color': 'blue', 'text-decoration': 'none'}),
    ], className = 'row'),
    
    html.Div([
            dash_table.DataTable(
            id = 'datatable_cases',
            data = dff.to_dict('records'),
            columns = [
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in dff.columns
            ],
            editable = False,
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            row_selectable = "multi",
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current =  0,
            page_size =  10,
            # page_action = 'none',
            # style_cell = {
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows = { 'headers': True, 'data': 0 },
            # virtualization = False,
            style_cell_conditional  = [
                {'if': {'column_id': 'Province/State'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'Country/Region'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'Country/Region'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'date'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'confirmed'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'death'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'recovered'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'active'},
                 'width': '10%', 'textAlign': 'left'},
            ], 
        ),
    ],className = 'twelve columns'),
    
    html.Div([
        html.H6("Data on COVID-19 (coronavirus) vaccinations by 'Our World in Data'", style = {"color": "white"}),
        html.P("Country-by-country data on global COVID-19 vaccinations", style = {"color": "white"}),
        dcc.Link(html.A('Data Source: Our World in Data'), href="https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('vaccinations.csv'), href="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv", style={'color': 'blue', 'text-decoration': 'none'}),
    ], className = 'row'),
    
    #vaccinesAnalysis
    html.Div([
            dash_table.DataTable(
            id = 'vaccinesAnalysis',
            data = dff2.to_dict('records'),
            columns = [
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in dff2.columns
            ],
            editable = False,
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            row_selectable = "multi",
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current =  0,
            page_size =  10,
            # page_action = 'none',
            # style_cell = {
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows = { 'headers': True, 'data': 0 },
            # virtualization = False,
            style_cell_conditional  = [
                {'if': {'column_id': 'location'},
                 'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'date'},
                 'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'people_fully_vaccinated'},
                 'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'daily_people_vaccinated'},
                 'width': '25%', 'textAlign': 'left'},
            ],
            
        ),
    ], className = 'twelve columns'),
    
    html.Div([
        html.P("Vaccinations by Manufacturer", style = {"color": "white"}),
        dcc.Link(html.A('Data Source: Our World in Data'), href="https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('vaccinations-by-manufacturer.csv'), href="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv", style={'color': 'blue', 'text-decoration': 'none'}),
    ], className = 'row'),
    
    #vaccinations-by-manufacturer
    html.Div([
            dash_table.DataTable(
            id = 'vaccinations-by-manufacturer',
            data = dff3.to_dict('records'),
            columns = [
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in dff3.columns
            ],
            editable = False,
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            row_selectable = "multi",
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current =  0,
            page_size =  10,
            # page_action = 'none',
            # style_cell = {
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows = { 'headers': True, 'data': 0 },
            # virtualization = False,
            style_cell_conditional  = [
                {'if': {'column_id': 'location'},
                 'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'date'},
                 'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'vaccine'},
                  'width': '25%', 'textAlign': 'left'},
                {'if': {'column_id': 'total_vaccinations'},
                  'width': '25%', 'textAlign': 'left'},
            ],
            
        ),
    ], className = 'twelve columns'),
    html.Div([
        html.P("Vaccinations by Age Group", style = {"color": "white"}),
        dcc.Link(html.A('Data Source: Our World in Data'), href="https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations", style={'color': 'blue', 'text-decoration': 'none'}),
        html.Br(),
        dcc.Link(html.A('vaccinations-by-manufacturer.csv'), href="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-age-group.csv", style={'color': 'blue', 'text-decoration': 'none'}),
    ], className = 'row'),
    
    #vaccinations-by-age-group  
    html.Div([
            dash_table.DataTable(
            id = 'vaccinations-by-age-group',
            data = dff4.to_dict('records'),
            columns = [
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in dff4.columns
            ],
            editable = False,
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            row_selectable = "multi",
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current =  0,
            page_size =  10,
            # page_action = 'none',
            # style_cell = {
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows = { 'headers': True, 'data': 0 },
            # virtualization = False,
            style_cell_conditional  = [
                {'if': {'column_id': 'location'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'date'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'age_group'},
                  'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'people_vaccinated_per_hundred'},
                  'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'people_fully_vaccinated_per_hundred'},
                  'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'people_with_booster_per_hundred'},
                  'width': '30%', 'textAlign': 'left'},
            ],
            
        ),
    ], className = 'twelve columns'),

])
