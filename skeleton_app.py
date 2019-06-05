#!/usr/bin/env python3                                                                     
# -*- coding: utf-8 -*- 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import base64
import datetime
import io
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Welcome to the Gene Expression Characterization Server',
            style={
                'textAlign': 'center'
                }
    ),

    html.Div('''
        Please input the file of  a line separated list of genes or uniprot codes or paste a list of genes in the box and select the output you would like
    ''',
        style={
                'textAlign': 'center'
               }
        ),
   
    html.Div([

    dcc.Upload(
        id='upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
            multiple=True
    ),
    html.Div([
        dcc.Textarea(
           placeholder='Enter a comma separated list of genes...',
           style={
                 'width':'50%'
           }
    ),

            html.Label('Please select the output you would like from the server and then press the submit button'),
            dcc.RadioItems(
                id='functions',
                options=[
                {'label': 'Fold', 'value': 'fold'},
                {'label': 'Family', 'value': 'family'},
                {'label': 'Super Family', 'value': 'super_family'},
                {'label': 'Domain', 'value': 'domain'}
                ]
                )
           ]),
    
    html.Hr(),
    
    html.Button('Submit', id='button'),
    html.Div(id='output_container_button')
    ])
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if filename[-3:] == 'csv':
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),
                usecols=[0],
                header=None)
        elif filename[-3:] == 'xls':
            df = pd.read_excel(io.BytesIO(decoded),
                usecols=[0],
                header=None)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df[0].tolist()

@app.callback(
    Output('output_container_button','children'),
    [Input('upload_data', 'contents'), 
     Input('upload_data', 'filename'),
     Input('functions', 'value'),
     Input('button', 'n_clicks')])

def update_output(list_of_contents, list_of_names, value, n_clicks):
    if n_clicks is not None:
        if list_of_contents is None:
            n_clicks = None
            return 'Please submit a file'
        if value is None:
            n_clicks = None
            return 'Please select an output'
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        for child in children:
            print(child)

if __name__ == '__main__':
    app.run_server(debug=True)
