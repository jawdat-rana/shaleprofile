# -*- coding: utf-8 -*-

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

application = app.server

#######################
# Functions


def get_chart_data(url):
    response = requests.get(url)

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        # if not 200
        raise "Error: " + str(e)

    json_obj = response.json()
    data_obj = json_obj['series'][0]['data']

    data = {"Years": [],
            "Billion Cubic Feet - BCF": []
            }

    for d in reversed(data_obj):
        data['Years'].append(d[0])
        data['Billion Cubic Feet - BCF'].append(d[1])

    return data


#######################
# Index Page

# table
df = pd.read_html("https://shale-gas-production.deta.dev/v1/shale/overview/?format=html")
df = df[0][['Area', '2015', '2016', '2017', '2018', '2019', '2020', 'series_id']]

# charts
arkansas_df = pd.DataFrame(get_chart_data('https://shale-gas-production.deta.dev/v1/shale/series/RES_EPG0_R5302_SAR_BCF.A'))
arkansas_chart = px.line(arkansas_df, x="Years", y="Billion Cubic Feet - BCF")

texas_df = pd.DataFrame(get_chart_data('https://shale-gas-production.deta.dev/v1/shale/series/RES_EPG0_R5302_STX_BCF.A'))
texas_chart = px.line(texas_df, x="Years", y="Billion Cubic Feet - BCF")

# page layout
index_page = html.Div([
    html.H1(children='Shale Gas Production'),
    html.Br(),
    html.Div(children='''
    This data has been taken from the following portal:
    '''),
    dcc.Link('U.S. Energy Information Administration', href='https://www.eia.gov/dnav/ng/ng_prod_shalegas_s1_a.htm'),
    html.Div(children='''
        My initial plan was to create a table with links to individual pages of Area - unfortunately table is generated 
        by a library and it doesn't seem to like modifications to it. Maybe there is I haven't explored the option in detail.
        For reference I have added two charts below the table to give you an idea of how it would look like on a separate page. 
    '''),
    html.Br(),
    html.Br(),
    html.Br(),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=20,
    ),
    html.Br(),
    html.H3('Arkansas Shale Production, Annual'),
    dcc.Graph(
        id='Shale Production - Arkansas',
        figure=arkansas_chart
    ),
    html.Br(),
    html.H3('Texas (with State Offshore) Shale Production, Annual'),
    dcc.Graph(
        id='Shale Production - Texas',
        figure=texas_chart
    ),
])

app.layout = index_page


if __name__ == '__main__':
    application.run(debug=True, port=8080)
