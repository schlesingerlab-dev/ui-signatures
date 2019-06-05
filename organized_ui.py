#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################
#Imports/Set UP
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State

import base64
import datetime
import io
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#################
#Functions


#################
# App Layout
app.layout = html.Div([
        html.Div([ 
                html.Div([
                        # Headings for Page
                        html.H1(
                            'Welcome to the Gene Expression Characterization Server',
                            style={
                                'textAlign': 'center'
                            }
                        ),
                        html.P(
                            '(Description of what structural signatures does)',
                            style={
                                'textAlign': 'center'
                            }
                        ),
                        html.Hr()
                ]),
                html.Div([
                        #File/list input
                        html.Label(
                            'Please input the file of  a line separated list of genes or uniprot codes or paste a list of genes in the box and select the output you would like',
                            style={
                                'textAlign': 'center'
                            }
                        ),
                        dcc.Upload(
                            id='upload_data_dragdrop',
                            children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                    ]),
                            style={
                                'width': '47%',
                                'height': '150px',
                                'lineHeight': '150px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px',
                                'float': 'left'
                            },
                            multiple=True
                        ),
                        dcc.Textarea(
                            id='upload_data_paste',
                            placeholder='Enter a comma separated list of genes...',
                            style={
                                'width':'47%',
                                'height':'150px',
                                'borderWidth': '1px',
                                'borderRadius': '5px',
                                'margin': '11px',
                                'float': 'right'
                            }
                        ),
                ]),
                html.Div([
                        html.Label(
                            'Please select the output you would like from the server and then press the submit button',
                            style={
                                'marginTop':'180px'
                            }
                         ),
                        dcc.Checklist(
                            id='divisions_to_use',
                            options=[
                                {'label': 'Fold', 'value': 'fold'},
                                {'label': 'Family', 'value': 'family'},
                                {'label': 'Super Family', 'value': 'super_family'},
                                {'label': 'Domain', 'value': 'domain'}
                             ],
                            values=[],
                            labelStyle={
                                'display':'inline-block',
                                'margin': '16px'
                            }
                         )
               ]),
                html.Div([
                        html.Label(
                            'Please select whether you would like a 2D or 3D signature'
                        ),
                        dcc.RadioItems(
                            id='dimension',
                            options=[
                                {'label':'2D', 'value':'2d'},
                                {'label':'3D', 'value': '3d'}
                            ]
                        ),
                        html.Label(
                            'Please select the number of bootstraps'
                        ),
                        dcc.Input(
                            id='n_bootstraps',
                            placeholder='Enter a number...',
                            type='number',
                            min=0
                        ),
                        html.Label(
                            'Please select the number of parallel processes (the maximum number is 4)'
                        ),
                        dcc.Input(
                            id='n_para_process',
                            placeholder='Enter a number between 0 and 4...',
                            type='number',
                            min=0,
                            max=4
                        )
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
