# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:21:38 2020

@author: Jaiswalji
"""
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import time


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])


def load_data():
  dataset_name = "global_terror.csv"
  
  global df
  df = pd.read_csv(dataset_name)
  
  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]


  global country_list

  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  global state_list
 
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()


  global city_list

  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  #print(year_dict)
  
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
def open_browser():
  webbrowser.open_new('http://127.0.0.1:8050/')


def create_app8_ui():

  main_layout = html.Div([
  html.H1('Terrorism Analysis with Insights', id='Main_title',style={'text-align':'center',
                                                                     'color':'#FF5733   ',
                                                                      'background-color': 'red',
                                                                      'background-image' :'url(data:image/jpeg;base64,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)'}),
  html.Br(),
  dcc.Tabs(id="Tabs", value="Map",children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
              ]),
          html.Br(),
          dcc.Dropdown(
              id='month', 
                options=month_list,
                placeholder='Select Month',
                multi = True,
                style={'border-radius' : '40px',
                       'height' : '40px',
                       'font-size' : '38',
                       'font-family': 'Comic Sans MS'},


                  ),
          html.Br(),
          dcc.Dropdown(
                id='date', 
                placeholder='Select Day',
                multi = True,        
                style={'border-radius' : '40px'},

                  ),
          html.Br(),
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True,
                style={'border-radius' : '40px'},

                  ),
          html.Br(),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select Country',
                multi = True,         
                style={'border-radius' : '40px'},

                  ),
          html.Br(),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True,                   
                style={'border-radius' : '40px'},

                  ),
          html.Br(),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True,
                style={'border-radius' : '40px',
                       },

                  ),
          html.Br(),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                placeholder='Select Attack Type',
                multi = True,
                style={'border-radius' : '40px'},

                  ),
          html.Br(),
          html.H5('Select the Year', id='year_title'),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Hr(),
            html.Br(),
            
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]),
         ]),
  html.Br(),

  html.Div(id = "graph-object",  
           children=dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="cube",
                    fullscreen=True
                   
                ))
  ])
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('cyear_slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )

def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1,
         
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count",color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)


@app.callback(Output("loading-output-2", "children"), [Input("graph-object", "value")])
def input_triggers_nested(value):
    time.sleep(100)
    return value


@app.callback(
  Output("date", "options"),
  [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

def main8():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app8_ui()
  app.title = "Terrorism Analysis with Insights"
  app.run_server()

  print("File was Closed")
  df = None
  app = None



if __name__ == '__main__':
    main8()