#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################
# App Description
'''
This page allows the user to explore the database 
'''

################
#Imports/Set UP

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import string
import random
import subprocess
import os
import urllib.parse
import dash_table
import pandas as pd
from app import app

#################
#Functions


#################
# App Layout

layout = html.Div([

    html.Div([
        #nav bar
        html.Nav(
            html.Div(
                children=[
                    #nav bar title
                    html.A(
                        'Structural Signatures',
                        className='brand-logo',
                        href='/'
                    ),
                    #ul list components
                    html.Ul(
                        children=[
                            html.Li(html.I(id='home',  className='fa fa-home')),
                            html.Li(html.A('Home', href='/')),
                            html.Li(html.I(id='search',  className='fa fa-search')),
                            html.Li(html.A('Data Explorer', href='/apps/databasenav')),
                            html.Li(html.I(id='search',  className='fa fa-asterisk')),
                            html.Li(html.A('Generate Structural Signatures', href='/apps/app1')), 
                            html.Li(html.I(id='search',  className='fa fa-users')),
                            html.Li(html.A('About', href='/apps/about')), 
                        ],
                        id='nav-mobile',
                        className='right hide-off-med-and-down'
                    ), 
                ],
                className='nav-wrapper'
            ),
            style={'background-color':'#4c586f'}),
        ],
    className='navbar-fixed'
    ),
    html.Div([
        html.H6(
            'Select the database you would like to search',
            style={
                'marginLeft':'11px',
                'marginTop': '11px'
            }
        ),
        dcc.RadioItems(
            id='database_name',
            options=[
                {'label':'gTEx', 'value':'gtex'},
                {'label':'ARCHS', 'value': 'archs'}
                
            ],
            style={
                'margin':'11px'
            }
        ),
        html.Div([
            # search database
            dcc.Input(
                id='search_text',
                style={
                    'marginLeft':'11px',
                    'marginBottom':'20px'
                }
            ),
            html.Button(
                'Search',
                id='search_submit',
                style={
                    'marginBottom':'20px'
                }
            )
        ]),
        dash_table.DataTable(
            id='database_display'
        ),
        html.H6(
            id='database_error',
            children='The value you searched for could not be found',
            style={
                'display':'none'
            }
        )
    ])
])


################
# Callbacks

# displays searchable database table 
@app.callback(
    [Output('database_display', 'columns'),
     Output('database_display', 'data')],
    [Input('database_name', 'value'),
     Input('search_text', 'value')]
    )

def display_table(database_name, search_name):
    if database_name == 'gtex':
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
        if search_name:
            df_rows = df.loc[df['State'].str.contains(search_name)]
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
        if search_name:
            df_rows = df.loc[df['country'].str.contains(search_name)]

    if not search_name:
        df_rows = df

    return [
        [{"name": i, "id": i} for i in df.columns],
        df_rows.to_dict('records')
    ]

@app.callback(
    Output('database_error', 'style'),
    [Input('database_display', 'data')]
    )

def database_search_error(database_data):
    if database_data == []:
        return {}
    return {'display':'none'}