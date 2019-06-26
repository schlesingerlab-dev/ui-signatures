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

# load the databases
df_dict = {}
structure_types = ['domain', 'family', 'fold', 'superfam']

for structure in structure_types:
    df_dict['gtex_'+structure] = pd.read_csv('./bin/table_data_explorer/GTeX_ss/allcombined.250.' + structure + '.csv.3',
                                names=['Structure', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', ' p value', 'FDR', 'Bonforroni', 'Log Fold Change', 'Sample ID', 'Subtissue', 'Organ'])
    # split the last row of the archs data and adds it to the dictionary of databases
    edit_archs = pd.read_csv('./bin/table_data_explorer/ARCHS4_ss/allcombined.archs4.' + structure + '.csv',
    names=['Structure', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', ' p value', 'FDR', 'Bonforroni', 'Log Fold Change', 'temp'])
    edit_archs[['Sample ID', 'Organ']] = edit_archs.temp.str.split('-',expand=True)
    df_dict['archs_'+structure] = edit_archs

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
    # select the database to display data from
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
            value='gtex',
            style={
                'margin':'11px'
            }
        ),
        # search table
        html.H6(
            'Select the field you would like to search:'
        ),
        dcc.RadioItems(
            id='search_type_gtex',
            options=[
                {'label':'Structure', 'value':'Structure'},
                {'label':'Sample ID', 'value': 'Sample ID'},
                {'label':'Subtissue', 'value':'Subtissue'},
                {'label':'Organ', 'value':'Organ'}
                
            ],
            value='Structure',
            style={
                'margin':'11px'
            }
        ),
        dcc.RadioItems(
            id='search_type_archs',
            options=[
                {'label':'Structure', 'value':'Structure'},
                {'label':'Sample ID', 'value': 'Sample ID'},
                {'label':'Organ', 'value':'Organ'}
                
            ],
            value='Structure',
            style={
                'margin':'11px'
            }
        ),
        html.Div([
            # Search table input
            dcc.Input(
                id='search_table',
                style={
                    'marginLeft':'11px',
                    'marginBottom':'22px',
                    'marginTop': '22px'
                }
            ),
        ]),
        # show whether you want to see data for family, fold, superfamily, or domain
        dcc.Tabs(
            id='class_tabs',
            value='domain',
            vertical=False,
            children=[
                dcc.Tab(label='Domain', value='domain'),
                dcc.Tab(label='Fold', value='fold'),
                dcc.Tab(label='Family', value='family'),
                dcc.Tab(label='Superfamily', value='superfam')
            ]
        ),
        # data table
        dash_table.DataTable(
            id='database_display'
        ),
        # shows if there is no data in the database
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

@app.callback(
    [Output('search_type_gtex', 'style'),
     Output('search_type_archs', 'style')],
    [Input('database_name', 'value')]
)

def search_option_update(database_name):
    if database_name == 'gtex':
        return [{}, {'display':'none'}]
    return [{'display':'none'}, {}]

# displays searchable database table 
@app.callback(
    [Output('database_display', 'columns'),
     Output('database_display', 'data')],
    [Input('database_name', 'value'),
     Input('class_tabs', 'value'),
     Input('search_table', 'value')],
     [State('search_type_gtex', 'value'),
      State('search_type_archs', 'value')]
    )

def display_table(database_name, class_type, search_value, search_type_gtex, search_type_archs):
    if database_name == 'gtex':
        search_type_value = search_type_gtex
    else:
        search_type_value = search_type_archs

    df_all = df_dict[database_name + '_' + class_type]
    if search_value:
        df = df_all.loc[df_all[search_type_value].str.contains(search_value)]
        df = df.head(10)
    else:
        df = df_all.head(10)
    return[
        [{"name": i, "id": i} for i in df.columns],
        df.to_dict('records')
    ]

# database error if no data in the database to display
@app.callback(
    Output('database_error', 'style'),
    [Input('database_display', 'data')]
    )

def database_search_error(database_data):
    if database_data == []:
        return {}
    return {'display':'none'}


