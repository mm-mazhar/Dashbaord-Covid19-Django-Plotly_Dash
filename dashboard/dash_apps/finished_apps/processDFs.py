from dashboard.dash_apps.finished_apps.extractData import covid_data, covid_data_1, covid_data_list, total_confirmed, total_deaths
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


#======= Renaming Columns in df 'covid_data'=======================================================================
covid_data.rename(columns={'province_state': 'Province/State',
                            'country_region': 'Country/Region',
                            'lat': 'Lat',
                            'long': 'Long',
                            'date': 'Date',
                            'confirmed': 'Confirmed', 
                            'death': 'Death',
                            'recovered': 'Recovered',
                            'active': 'Active'}, inplace = True)
#print(covid_data.columns)
#======/ Renaming Columns in df 'covid_data'==========================================================================

#======= Renaming Columns in df 'covid_data_1'=======================================================================
covid_data_1.rename(columns={'date': 'Date',
                            'confirmed': 'Confirmed', 
                            'death': 'Death',
                            'recovered': 'Recovered',
                            'active': 'Active'}, inplace = True)
#print(covid_data.columns)
#======/ Renaming Columns in df 'covid_data_1'==========================================================================

#======= Renaming Columns in df 'covid_data_list'=======================================================================
covid_data_list.rename(columns={'country_region': 'Country/Region',
                                'lat': 'Lat',
                                'long': 'Long'}, inplace = True)
#print(covid_data.columns)
#======/ Renaming Columns in df 'covid_data_list'==========================================================================

#=======Converting Data Types of df 'covid_data=======================================================================
covid_data_DataTypes_dict = {'Province/State': str, 
                        'Country/Region': str, 
                        'Lat': float, 
                        'Long': float, 
                        'Date': str, 
                        'Confirmed': int, 
                        'Death': int, 
                        'Recovered': int, 
                        'Active': int
                        }

covid_data_1_DataTypes_dict = {'Date': str, 
                        'Confirmed': int, 
                        'Death': int, 
                        'Recovered': int, 
                        'Active': int
                        }

covid_data_list_DataTypes_dict = {'Country/Region': str, 
                        'Lat': float, 
                        'Long': float, 
                        }

covid_data = covid_data.astype(covid_data_DataTypes_dict)
covid_data['Date'] = pd.to_datetime(covid_data['Date'])

#covid_data_1 = covid_data_1.infer_objects()
covid_data_1 = covid_data_1.astype(covid_data_1_DataTypes_dict)

covid_data_list = covid_data_list.astype(covid_data_list_DataTypes_dict)
#=======/ Converting Data Types of df 'covid_data=======================================================================

dict_of_locations = covid_data_list.set_index('Country/Region')[['Lat', 'Long']].T.to_dict('dict')

# print("Data Types of covid_data:\n", covid_data.dtypes)
# print("\n")
# print("Data Types of covid_data_1:\n", covid_data_1.dtypes)
# print("\n")
# print("Data Types of covid_data_list:\n", covid_data_list.dtypes)
# print("\n")
# print("Dict of Locations:\n", covid_data_list.dtypes)
# print("\n")
#print("Covid_data_: \n", covid_data_1.tail())

# print("\n")
# print("Total Confirmed: \n", total_confirmed.tail())

#======= Processing dfc for animationConfirmedCases.py =======================================================================
#Drop unnecessary columns
total_confirmed.drop(['Lat', 'Long'], axis = 1, inplace = True) 

total_confirmed['Date'] = pd.to_datetime(total_confirmed['date'], errors='coerce')
total_confirmed['Month'] = total_confirmed['Date'].dt.strftime('%m')
total_confirmed['Year'] = total_confirmed['Date'].dt.strftime('%Y')

dfc = total_confirmed.groupby(['Country/Region', 'Month', 'Year']).max('confirmed').reset_index()

dfc['MonthYear'] = dfc[['Month', 'Year']].agg('-'.join, axis = 1)

year = dfc['Year'].unique()
year = year.tolist()
year = sorted(year, reverse = False)

month = dfc['Month'].unique()
month = month.tolist()
month = sorted(month, reverse = False)

month_year = []
for i in year:
    for k in month:
        month_year.append(k + '-' + i)
        

dict_keys = list(map(str, month_year))

#print(month_year)  #export to covidAnimation.py
#print(dict_keys)   #export to covidAnimation.py

dict_of_color_codes = {'Afghanistan': '#000000', 'Albania': '#321FFF', 'Algeria': '#FF0000', 'Andorra': '#FFFF00', 'Angola': '#FF00FF', 
                       'Antigua and Barbuda': '#00FFFF', 'Argentina': '#800000', 'Armenia': '#008000', 'Australia': '#808000', 'Austria': '#800080', 
                       'Azerbaijan': '#008080', 'Bahamas': '#C0C0C0', 'Bahrain': '#808080', 'Bangladesh': '#9999FF', 'Barbados': '#993366', 
                       'Belarus': '#FFFFCC', 'Belgium': '#CCFFFF', 'Belize': '#660066', 'Benin': '#FF8080', 'Bermuda': '#0066CC', 'Bhutan': '#CCCCFF', 
                       'Bolivia': '#000080', 'Bosnia and Herzegovina': '#FF00FF', 'Botswana': '#FFFF00', 'Brazil': '#00FFFF', 'Brunei': '#800080', 
                       'Bulgaria': '#800000', 'Burkina Faso': '#008080', 'Burundi': '#FFFF00', 'Cambodia': '#00CCFF', 'Cameroon': '#CCFFFF', 
                       'Canada': '#CCFFCC', 'Cape Verde': '#FFFF99', 'C. African Rep.': '#FF99CC', 'Chad': '#FFCC00', 'Chile': '#FF9900', 
                       'China': '#FF6600', 'Colombia': '#666699', 'Comoros': '#969696', 'Congo': '#333333', 'Costa Rica': '#339966', 
                       "Cote d'Ivoire": '#003300', 'Croatia': '#333300', 'Cuba': '#993300', 'Cyprus': '#993366', 'Czech Republic': '#333399', 
                       'Denmark': '#808080', 'Djibouti': '#9999FF', 'Dominica': '#993366', 'Dominican Republic': '#FFFFCC', 'Ecuador': '#0066CC', 
                       'Egypt': '#CCCCFF', 'ElSalvador': '#000080', 'England': '#FF00FF', 'Equatorial Guinea': '#FFFF00', 'Eritrea': '#00FFFF', 
                       'Estonia': '#800080', 'Ethiopia': '#800000', 'Fiji': '#008080', 'Finland': '#0000FF', 'France': '#00CCFF', 'Gabon': '#CCFFFF', 
                       'Gambia': '#CCFFCC', 'Georgia': '#FFFF99', 'Germany': '#99CCFF', 'Ghana': '#FF99CC', 'Greece': '#CC99FF', 'Greenland': '#FFCC99', 
                       'Grenada': '#3366FF', 'Guam': '#33CCCC', 'Guatemala': '#99CC00', 'Guinea': '#FFCC00', 'Guinea-Bissau': '#FF9900', 'Guyana': '#FF6600', 
                       'Haiti': '#666699', 'Honduras': '#333300', 'Hungary': '#993300', 'Iceland': '#993366', 'India': '#333399', 'Indonesia': '#000000', 
                       'Iran': '#993366', 'Iraq': '#FF0000', 'Ireland': '#00FF00', 'Israel': '#0000FF', 'Italy': '#FFFF00', 'Jamaica': '#FF00FF', 
                       'Japan': '#00FFFF', 'Jordan': '#800000', 'Kazakhstan': '#008000', 'Kenya': '#000080', 'Kiribati': '#808000', 'Kuwait': '#800080', 
                       'Kyrgyzstan': '#008080', 'Laos': '#C0C0C0', 'Latvia': '#9999FF', 'Lebanon': '#993366', 'Lesotho': '#FFFFCC', 'Liberia': '#CCFFFF', 
                       'Libya': '#660066', 'Lithuania': '#FF8080', 'Luxembourg': '#000080', 'Macedonia': '#FF00FF', 'Madagascar': '#FFFF00', 'Malawi': '#00FFFF', 
                       'Malaysia': '#800080', 'Maldives': '#800000', 'Mali': '#008080', 'Malta': '#0000FF', 'Marshall Islands': '#00CCFF', 
                       'Mauritania': '#CCFFFF', 'Mauritius': '#CCFFCC', 'Mexico': '#FFFF99', 'Micronesia': '#99CCFF', 'Moldova': '#CC99FF', 
                       'Mongolia': '#FFCC99', 'Montenegro': '#3366FF', 'Morocco': '#33CCCC', 'Mozambique': '#99CC00', 'Myanmar': '#FFCC00', 
                       'Namibia': '#FF9900', 'Nepal': '#FF6600', 'Netherlands': '#666699', 'New Zealand': '#969696', 'Nicaragua': '#003366', 
                       'Niger': '#339966', 'Nigeria': '#003300', 'Korea\, North': '#993366', 'Norway': '#808080', 'Oman': '#993366', 
                       'Pakistan': '#FFFFCC', 'Palestine': '#CCFFFF', 'Panama': '#660066', 'Papua New Guinea': '#FF8080', 'Paraguay': '#0066CC', 
                       'Peru': '#CCCCFF', 'Philippines': '#000080', 'Poland': '#FF00FF', 'Portugal': '#FFFF00', 'Puerto Rico': '#00FFFF', 
                       'Qatar': '#800080', 'Romania': '#800000', 'Russia': '#008080', 'Rwanda': '#0000FF', 'Saint Lucia': '#00CCFF', 
                       'Saint Vincent and the Grenadines': '#CCFFFF', 'Samoa': '#CCFFCC', 'Sao Tome and Principe': '#FFFF99', 'Saudi Arabia': '#99CCFF', 
                       'Senegal': '#CC99FF', 'Serbia': '#FFCC99', 'Seychelles': '#3366FF', 'Sierra Leone': '#33CCCC', 'Singapore': '#99CC00', 
                       'Slovakia': '#FFCC00', 'Slovenia': '#FF9900', 'Solomon Islands': '#FF6600', 'Somalia': '#666699', 'South Africa': '#969696', 
                       'Korea\, South': '#339966', 'South Sudan': '#003300', 'Spain': '#000000', 'Sri Lanka': '#993366', 'Sudan': '#00FF00', 
                       'Suriname': '#0000FF', 'Swaziland': '#FFFF00', 'Sweden': '#FF00FF', 'Switzerland': '#00FFFF', 'Syria': '#800000', 
                       'Taiwan': '#008000', 'Tajikistan': '#000080', 'Tanzania': '#808000', 'Thailand': '#800080', 'Timor': '#008080', 
                       'Togo': '#C0C0C0', 'Tonga': '#808080', 'Tri. & Tobago': '#9999FF', 'Tunisia': '#FFFFCC', 'Turkey': '#CCFFFF', 
                       'Turkmenistan': '#660066', 'Uganda': '#FF8080', 'Ukraine': '#0066CC', 'United Arab Emirates': '#CCCCFF', 'United Kingdom': '#FF00FF',
                       'US': '#FF6347', 'Uruguay': '#00FFFF', 'Uzbekistan': '#800080', 'Vanuatu': '#800000', 'Venezuela': '#008080', 
                       'Vietnam': '#0000FF', 'Yemen': '#99CCFF', 'Zambia': '#FF99CC', 'Zimbabwe': '#CC99FF'}

dfc['color_code'] = dfc['Country/Region'].map(dict_of_color_codes)
dfc['color_code'] = dfc['color_code'].fillna('#111222')


dict_region = {'Afghanistan': 'Eastern Mediterranean', 'Albania': 'Europe', 'Algeria': 'Africa', 'Andorra': 'Europe', 'Angola': 'Africa', 
               'Antigua and Barbuda': 'Western Pacific', 'Argentina': 'Americas', 'Armenia': 'Europe', 'Australia': 'Western Pacific', 
               'Austria': 'Europe', 'Azerbaijan': 'Europe', 'Bahamas': 'Americas', 'Bahrain': 'Eastern Mediterranean', 'Bangladesh': 'South-East Asia', 
               'Barbados': 'Americas', 'Belarus': 'Europe', 'Belgium': 'Europe', 'Belize': 'Americas', 'Benin': 'Africa', 'Bermuda': 'Americas', 
               'Bhutan': 'South-East Asia', 'Bolivia': 'Americas', 'Bosnia and Herzegovina': 'Europe', 'Botswana': 'Africa', 'Brazil': 'Americas', 
               'Brunei': 'South-East Asia', 'Bulgaria': 'Europe', 'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cambodia': 'Western Pacific', 
               'Cameroon': 'Africa', 'Canada': 'Americas', 'Cape Verde': 'Africa', 'C. African Rep.': 'Africa', 'Chad': 'Africa', 'Chile': 'Americas', 
               'China': 'South-East Asia', 'Colombia': 'Americas', 'Comoros': 'Africa', 'Congo': 'Africa', 'Costa Rica': 'Americas', 
               "Cote d'Ivoire": 'Africa', 'Croatia': 'Europe', 'Cuba': 'Americas', 'Cyprus': 'Europe', 'Czech Republic': 'Europe', 'Denmark': 'Europe', 
               'Djibouti': 'Africa', 'Dominica': 'Americas', 'Dominican Republic': 'Americas', 'Ecuador': 'Americas', 'Egypt': 'Eastern Mediterranean', 
               'El Salvador': 'Americas', 'England': 'Europe', 'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa', 'Estonia': 'Europe', 
               'Ethiopia': 'Africa', 'Fiji': 'Western Pacific', 'Finland': 'Europe', 'France': 'Europe', 'Gabon': 'Africa', 'Gambia': 'Africa', 
               'Georgia': 'Europe', 'Germany': 'Europe', 'Ghana': 'Africa', 'Greece': 'Europe', 'Greenland': 'Europe', 'Grenada': 'Americas', 
               'Guam': 'Western Pacific', 'Guatemala': 'Americas', 'Guinea': 'Africa', 'Guinea-Bissau': 'Africa', 'Guyana': 'Americas', 
               'Haiti': 'Americas', 'Honduras': 'Americas', 'Hungary': 'Europe', 'Iceland': 'Europe', 'India': 'South-East Asia', 
               'Indonesia': 'South-East Asia', 'Iran': 'Eastern Mediterranean', 'Iraq': 'Eastern Mediterranean', 'Ireland': 'Europe', 
               'Israel': 'Eastern Mediterranean', 'Italy': 'Europe', 'Jamaica': 'Americas', 'Japan': 'Western Pacific', 
               'Jordan': 'Eastern Mediterranean', 'Kazakhstan': 'Europe', 'Kenya': 'Africa', 'Kiribati': 'Western Pacific', 
               'Kuwait': 'Eastern Mediterranean', 'Kyrgyzstan': 'Europe', 'Laos': 'South-East Asia', 'Latvia': 'Europe', 
               'Lebanon': 'Eastern Mediterranean', 'Lesotho': 'Africa', 'Liberia': 'Africa', 'Libya': 'Africa', 'Lithuania': 'Europe', 
               'Luxembourg': 'Europe', 'Macedonia': 'Europe', 'Madagascar': 'Africa', 'Malawi': 'Africa', 'Malaysia': 'Western Pacific', 
               'Maldives': 'South-East Asia', 'Mali': 'Africa', 'Malta': 'Europe', 'Marshall Islands': 'Western Pacific', 'Mauritania': 'Africa', 
               'Mauritius': 'Africa', 'Mexico': 'Americas', 'Micronesia': 'Western Pacific', 'Moldova': 'Europe', 'Mongolia': 'South-East Asia', 
               'Montenegro': 'Europe', 'Morocco': 'Africa', 'Mozambique': 'Africa', 'Myanmar': 'South-East Asia', 'Namibia': 'Africa', 
               'Nepal': 'South-East Asia', 'Netherlands': 'Europe', 'New Zealand': 'Western Pacific', 'Nicaragua': 'Americas', 'Niger': 'Africa', 
               'Nigeria': 'Africa', 'Korea\, North': 'South-East Asia', 'Norway': 'Europe', 'Oman': 'Eastern Mediterranean', 
               'Pakistan': 'Eastern Mediterranean', 'Palestine': 'Eastern Mediterranean', 'Panama': 'Americas', 'Papua New Guinea': 'Western Pacific', 
               'Paraguay': 'Americas', 'Peru': 'Americas', 'Philippines': 'Western Pacific', 'Poland': 'Europe', 'Portugal': 'Europe', 
               'Puerto Rico': 'Americas', 'Qatar': 'Eastern Mediterranean', 'Romania': 'Europe', 'Russia': 'Europe', 'Rwanda': 'Africa', 
               'Saint Lucia': 'Americas', 'Saint Vincent and the Grenadines': 'Americas', 'Samoa': 'Western Pacific', 'Sao Tome and Principe': 'Africa', 
               'Saudi Arabia': 'Eastern Mediterranean', 'Senegal': 'Africa', 'Serbia': 'Europe', 'Seychelles': 'Africa', 'Sierra Leone': 'Africa', 
               'Singapore': 'South-East Asia', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Solomon Islands': 'Western Pacific', 'Somalia': 'Africa', 
               'South Africa': 'Africa', 'Korea\, South ': 'South-East Asia', 'South Sudan': 'Africa', 'Spain': 'Europe', 'Sri Lanka': 'South-East Asia', 
               'Sudan': 'Africa', 'Suriname': 'Americas', 'Swaziland': 'Africa', 'Sweden': 'Europe', 'Switzerland': 'Europe', 
               'Syria': 'Eastern Mediterranean', 'Taiwan': 'South-East Asia', 'Tajikistan': 'Europe', 'Tanzania': 'Africa', 
               'Thailand': 'South-East Asia', 'Timor': 'South-East Asia', 'Togo': 'Africa', 'Tonga': 'Western Pacific', 'Tri. & Tobago': 'Americas', 
               'Tunisia': 'Eastern Mediterranean', 'Turkey': 'Europe', 'Turkmenistan': 'Europe', 'Uganda': 'Africa', 'Ukraine': 'Europe', 
               'United Arab Emirates': 'Eastern Mediterranean', 'United Kingdom': 'Europe', 'United States': 'Americas', 'Uruguay': 'Americas', 'Uzbekistan': 'Europe', 
               'Vanuatu': 'Western Pacific', 'Venezuela': 'Americas', 'Vietnam': 'South-East Asia', 'Yemen': 'Eastern Mediterranean', 
               'Zambia': 'Africa', 'Zimbabwe': 'Africa'}

dfc['region'] = dfc['Country/Region'].map(dict_region)
dfc['region'] = dfc['region'].fillna('Not Available')

#print(pd.isnull(dfc).sum())
#======= / Processing dfc for animationConfirmedCases.py =======================================================================

#======= Processing dfd for animationDeaths.py =================================================================================

total_deaths.drop(['Lat', 'Long'], axis = 1, inplace = True) 

total_deaths['Date'] = pd.to_datetime(total_deaths['date'], errors='coerce')
total_deaths['Month'] = total_deaths['Date'].dt.strftime('%m')
total_deaths['Year'] = total_deaths['Date'].dt.strftime('%Y')

dfd = total_deaths.groupby(['Country/Region', 'Month', 'Year']).max('death').reset_index()

dfd['MonthYear'] = dfd[['Month', 'Year']].agg('-'.join, axis = 1)

yearD = dfd['Year'].unique()
yearD = yearD.tolist()
yearD = sorted(yearD, reverse = False)

monthD = dfd['Month'].unique()
monthD = monthD.tolist()
monthD = sorted(monthD, reverse = False)

month_yearD = []
for i in yearD:
    for k in monthD:
        month_yearD.append(k + '-' + i)
        

dict_keysD = list(map(str, month_yearD))

dfd['color_code'] = dfd['Country/Region'].map(dict_of_color_codes)
dfd['color_code'] = dfd['color_code'].fillna('#111222')


dfd['region'] = dfd['Country/Region'].map(dict_region)
dfd['region'] = dfd['region'].fillna('Not Available')

#======= / Processing dfd for animationDeaths.py =================================================================================

#print(total_deaths)

