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

def input_valid(filename, gene_list, div_list, val_dimension, num_bootstraps, num_para_process, n_clicks):
    if n_clicks == None:
        return 'no clicks'
    if filename != None or gene_list != None:
        if filename:
            if filename[-3:] != 'csv' and filename[-3:] != 'xls':
                return 'The format of the submited file is incorrect. Please submit a ".csv" or a ".xls" file'
        if gene_list:
            if type(gene_list) == 'str':
                pass
    else:
        return 'Please input a file or a gene list'


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
                            'Input the file of  a line separated list of genes or uniprot codes or paste a list of genes in the box and select the output you would like',
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
                            }
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
                        #Choosing: fold, family, super family, and/or domain
                        html.Label(
                            'Select the output you would like from the server and then press the submit button',
                            style={
                                'marginTop':'180px',
                                'marginLeft': '11px'
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
                                'margin': '16px',
                                'marginLeft': '11px'
                            }
                         )
               ]),
                html.Div([
                        # Choosing signature dimesnionality (bootstraps and parallel only appear if 3D is chosen 
                        html.Label(
                            'Select whether you would like a 2D or 3D signature',
                            style={
                                'marginTop':'11px',
                                'marginLeft':'11px'
                            }
                        ),
                        dcc.RadioItems(
                            id='dimension',
                            options=[
                                {'label':'2D', 'value':'2d'},
                                {'label':'3D', 'value': '3d'}
                            ],
                            value=None,
                            style={
                                'marginLeft':'11px'
                            }
                        ),
                        html.Label(
                            'Select the number of bootstraps',
                            id='bootstraps_label',
                            style={
                                'display':'none'
                                }
                        ),
                        dcc.Input(
                            id='n_bootstraps',
                            placeholder='Enter a number...',
                            type='number',
                            min=0,
                            style={
                                'display':'none',
                                'width':'35%'
                            }
                        ),
                        html.Label(
                            'Select the number of parallel processes (the maximum number is 4)',
                            id='para_process_label',
                            style={
                                'display':'none'
                            }
                        ),
                        dcc.Input(
                            id='n_para_process',
                            placeholder='Enter a number between 0 and 4...',
                            type='number',
                            min=0,
                            max=4,
                            style={
                                'display':'none',
                                'width':'35%'
                            }
                        )
                ]),
                html.Div([
                        # Input name of job (filename to export to)
                        html.Label(
                            'Submit the name of the job (the filename the job will be exported to)',
                            style={
                                'margin':'11px',
                                'marginTop':'27px'
                            }
                        ),
                        dcc.Input(
                            id='output_name',
                            style={
                                'marginLeft':'11px',
                                'width':'35%'
                            }
                        )
                ]),
                html.Div([
                        # Submit button
                        html.Hr(),
                        html.Button(
                            'Submit',
                            id='submit_button',
                            style={
                                'marginLeft':'43%',
                                'marginRight':'43%'
                            }
                        )
                ]),
                html.Div(
                        # Structural signatures output to return to user
                        id='struct_sig_output'
                ),
                html.Div([
                        #footer so I dont hit undo at bottom of page
                        html.Hr(),
                        html.Hr()
                ])
        ])
])

################
# Callbacks

# Allows the bootstraps and number of parrallel process selection options to appear after 3D is selected
@app.callback(
    [Output('bootstraps_label', 'style'),
     Output('n_bootstraps', 'style'),
     Output('para_process_label', 'style'),
     Output('n_para_process', 'style')],
    [Input('dimension', 'value')]
    )

def update_style(dimension):
    if dimension != '3d':
        return [{'display':'none'},
                {'display':'none'},
                {'display':'none'},
                {'display':'none'}]
    return[{'display':'block', 'margin':'11px', 'marginTop':'27px'},
           {'display':'block', 'marginLeft':'11px', 'width':'35%'},
           {'display':'block', 'margin':'11px', 'marginTop':'27px'},
           {'display':'block', 'marginLeft':'11px', 'width':'35%'}]

# Runs structural signatures in response to 'Submit' button press
@app.callback(
    Output('struct_sig_output','children'),
    [Input('upload_data_dragdrop', 'contents'),
     Input('upload_data_dragdrop', 'filename'),
     Input('upload_data_paste', 'value'),
     Input('divisions_to_use', 'values'),
     Input('dimension', 'value'),
     Input('n_bootstraps', 'value'),
     Input('n_para_process', 'value'),
     Input('output_name', 'value'),
     Input('submit_button', 'n_clicks')
     ]
    )

def update_output(content, filename, gene_list, div_list, val_dimension, num_bootstraps, num_para_process, name_file_out, n_clicks):
    return input_valid(filename, gene_list, div_list, val_dimension, num_bootstraps, num_para_process, n_clicks)

    

if __name__ == '__main__':
    app.run_server(debug=True)
