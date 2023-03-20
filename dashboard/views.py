import warnings
warnings.filterwarnings("ignore")
from multiprocessing import context
from django.shortcuts import render
from dashboard.dash_apps.finished_apps.processDFs import covid_data, covid_data_1
from dashboard.dash_apps.finished_apps.dropdownPieBarLineMap import *
from dashboard.dash_apps.finished_apps.deathRace import *
from dashboard.dash_apps.finished_apps.vaccinesAnalysis import *
from dashboard.dash_apps.finished_apps.vaccineManufacturer import *
from dashboard.dash_apps.finished_apps.vaccinations_by_age_group import *
from dashboard.dash_apps.finished_apps.dataTables import *

#from dashboard.dash_apps.finished_apps.simpleExample import *
import pandas as pd


# Create your views here.
def cases(request):
    context = {'lastUpdated': last_updated,
               'globalCases': global_cases,
               'percentChangeConfirmed': percent_change_confirmed,
               'globalDeaths': global_deaths,
               'percentChangeDeaths': percent_change_deaths,
               'globalRecovered': global_recovered,
               'percentChangeRecovered': percent_change_recovered,
               'globalActive': global_active,
               'percentChangeActive': percent_change_active,}
    
    return render(request, 'dashboard/covidCases.html', context = context)

#vaccinesAnalysis
def vaccinesAnalysis(request):
    context = {'lastUpdatedVaccines': last_updated_vaccines}    
    return render(request, 'dashboard/vaccinesAnalysis.html', context = context)

#deathRaceGraphs
def deathRace(request):
    context = {}
    return render(request, 'dashboard/deathRace.html', context = context)

#tables
def data(request):
    context = {}    
    return render(request, 'dashboard/data.html', context = context)

#contact
def contact(request):
    context = {}    
    return render(request, 'dashboard/contact.html', context = context)


# ==> def dashboard ==> dashboard.html file
last_updated = str(covid_data['Date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)'

global_cases = f"{covid_data_1['Confirmed'].iloc[-1]:,}"

percent_change_confirmed = "new: " + f"{covid_data_1['Confirmed'].iloc[-1] - covid_data_1['Confirmed'].iloc[-2]:,}" \
                    + " " +"(" + str(round(((covid_data_1['Confirmed'].iloc[-1] - covid_data_1['Confirmed'].iloc[-2]) \
                                            / covid_data_1['Confirmed'].iloc[-1]) * 100, 2)) + '%' + ")"

global_deaths = f"{covid_data_1['Death'].iloc[-1]:,}"

percent_change_deaths = 'new: ' + f"{covid_data_1['Death'].iloc[-1] - covid_data_1['Death'].iloc[-2]:,}" \
                   + ' (' + str(round(((covid_data_1['Death'].iloc[-1] - covid_data_1['Death'].iloc[-2]) / \
                                   covid_data_1['Death'].iloc[-1]) * 100, 2)) + '%)'

global_recovered = f"{covid_data_1['Recovered'].iloc[-1]:,}"

percent_change_recovered = 'new: ' + f"{covid_data_1['Recovered'].iloc[-1] - covid_data_1['Recovered'].iloc[-2]:,}" \
                   + ' (' + str(round(((covid_data_1['Recovered'].iloc[-1] - covid_data_1['Recovered'].iloc[-2]) /  \
                                   covid_data_1['Recovered'].iloc[-1]) * 100, 2)) + '%)'

global_active = f"{covid_data_1['Active'].iloc[-1]:,}"

percent_change_active = 'new: ' + f"{covid_data_1['Active'].iloc[-1] - covid_data_1['Active'].iloc[-2]:,}" \
                   + ' (' + str(round(((covid_data_1['Active'].iloc[-1] - covid_data_1['Active'].iloc[-2]) /    \
                                   covid_data_1['Active'].iloc[-1]) * 100, 2)) + '%)'
                   
#vaccinesAnalysis.py
dfcopy['date'] =  pd.to_datetime(dfcopy['date'], format = '%Y-%m-%d')
last_updated_vaccines = str(dfcopy['date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)'
