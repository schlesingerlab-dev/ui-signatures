#!/usr/bin/env python3                                                                                # -*- coding: utf-8 -*- 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Welcome to the Gene/Uniprot Expression Characterization Server'),

    html.Div('''
        Please input the file of  a line separated list of genes or uniprot codes and select the output you would like
    '''),
   
    html.Div([
            html.Label('File Name'),
            dcc.Input(id='file_name', value=None, type='text'),

            html.Label('Please select the outputs you would like from the server (it is possible to select more than one) and then press the submit button'),
            dcc.Dropdown(
                id='functions',
                options=[
                {'label': 'Meta-Signatures', 'value': 'metasig'},
                {'label': 'Future Options', 'value': 'TBD'}
                ],
                value=[],
                multi=True)
           ]),

    html.Button('Submit', id='button'),
    html.Div(id='output_container_button',
             children='Enter a value and press submit')

    ])

@app.callback(
    Output('output_container_button','children'),
    [Input('button', 'n_clicks'),
     Input('file_name', 'value'),
     Input('functions', 'value')])

#    Output('output-container-button', 'children'),
#    [Input('button', 'n_clicks'),
#     Input('functions','value')],
#    [State('file_name', 'value')])

def update_output(n_clicks, file_name, functions):
    if n_clicks != None:
        return 'The input file  was "{}" and the actions selected are {} '.format(
        file_name,
        functions
        )


if __name__ == '__main__':
    app.run_server(debug=True)
