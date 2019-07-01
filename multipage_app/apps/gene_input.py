#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################
# App Description
'''
This page takes user input for structural signatures
checks if there is input, 
and sends user to 'calculating page' (struct_sig_run_check.py) 
'''

################
#Imports/Set UP

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import string
import random
import subprocess
import os
import urllib.parse
from app import app

#################
#Functions

def gene_file_from_list(gene_list, name_paste_gene_file):
    '''
    Inputs:
        gene_list: (str) comma and/or separated string of gene names or uniprot IDs
        name_paste_gene_file: (str) refers to an already existing file
    
    Outputs:
        None, but adds to a line separated file of genes

    Description:
        genereates a file of line separated genes from the gene_list without duplicate genes
    '''
    f = open(name_paste_gene_file, 'a')
    gene = ''

    # For duplicate check
    duplicates = set()

    # Generate file
    for index in range(len(gene_list)):
        if gene_list[index] == ' ' or gene_list[index] == ',':
            if len(gene) > 0 and gene not in duplicates:
                f.write(gene + '\n')
                duplicates.add(gene)
            gene = ''
        else:
            gene += gene_list[index]
            if index == (len(gene_list)-1) and gene not in duplicates:
                f.write(gene + '\n')
                duplicates.add(gene)
                gene = ''
    f.close()

def gene_file_from_file(contents, name_local_file_from_file):
    '''
    Inputs:
        contents: file contents
        name_local_file_from_file: (str) refers to an already existing file
    
    Outputs:
        None, but adds to a line separated file of genes

    Description:
        appends the contents to the end of the file given
    '''
    f = open(name_local_file_from_file, 'a')
    splitting = contents.split(',')
    byte_represent = base64.b64decode(splitting[1])
    decoded = byte_represent.decode("utf-8") 
    f.write(decoded + '\n')
    f.close()

def contents_valid(contents):
    '''
    Input:
        contents: (str) contents of the file uploaded (to be checked)
    
    Output:
        (bool) whether or not the file contents are valid

    Description:
        checks for line separated gene names or uniprot codes
        (assumes gene names have no spaces and that there are no commas)
    '''
    splitting = contents.split(',')
    byte_represent = base64.b64decode(splitting[1])
    decoded = byte_represent.decode("utf-8") 
    line_index = decoded.find('\n')
    if ',' in decoded[:line_index] or decoded[len(decoded)-1] == ',' or ' ' in decoded[:line_index]:
        return False
    return True
         
def input_valid(filename, file_contents, gene_list, val_dimension, num_bootstraps, num_para_process):
    '''
    Input:
        file_contents: (str) contains the content of the inputed file
        gene_list: (str) user input of gene names or uniprot codes
        div_list: (list) contains info about structural divisons (family, superfamily, ...) the user wants computed
        val_dimension: (str) either '2d' or '3d'
        num_bootstraps: (int)
        num_para_process: (int) number of processes to run in parallel in structural signatures
    
    Output:
        (str) error message asking user for correct input
        True: (bool) if all of the checks pass
    
    Description:
        checks if all of the user inputs are valid
    '''
    # checks if there are files or gene list
    if filename or gene_list:
        if filename:
            if not contents_valid(file_contents):
                return 'The format of the submited file is incorrect. Please submit a file with line separated values'
    else:
        return 'Please input a file or a gene list'
    # checks for things needed for 3D input (the program does not deal with default values for these at this time)
    if val_dimension == '3d':
        if num_bootstraps == None:
            return 'Please select a positive integer for the number of bootstraps'
        if num_para_process == None:
            return 'Please select a number of parellel processes between 0 and 4'
    return True

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
                                    # html.Li(html.I(id='search',  className='fa fa-users')),
                                    # html.Li(html.A('About', href='/apps/about')), 
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
                # Headings for Page
                html.H1(
                    'Welcome to the Gene Expression Characterization Server',
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.P(
                    'Identification of robust gene expression signatures using protein structure enrichment and machine learning',
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Hr()
            ]),
            #File/list input
            html.H6(
                'Input the file of  a line separated list of genes or uniprot codes or paste a list of genes in the box and select the output you would like',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            dcc.Upload(
                                id='upload_data_dragdrop',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select File')
                                    ]),
                                style={
                                    'width': '95%',
                                    'height': '150px',
                                    'lineHeight': '150px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '11px',
                                } 
                            ),
                        ),
                        html.Div(
                            html.H6(
                                id='file_name_display',
                                children='None',
                                style={
                                    'width': '95%',
                                    'height': '65px',
                                    'lineHeight': '65px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'solid',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '11px',
                                    'display': 'none'
                                } 
                            )
                        ),
                        html.Div(
                            html.Button(
                                'Select different file',
                                id='file_change_select',
                                style={
                                    'width': '95%',
                                    'height': '65px',
                                    'lineHeight': '65px',
                                    'borderWidth': '1px',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '11px',
                                    'display':'none'           
                                }
                            )
                        )
                    ]),
                    dbc.Col(
                        html.Div(
                            dcc.Textarea(
                                    id='upload_data_paste',
                                    placeholder='Enter a comma separated list of genes...',
                                    style={
                                        'width':'95%',
                                        'height':'150px',
                                        'borderWidth': '1px',
                                        'borderRadius': '5px',
                                        'margin': '11px',
                                    }
                            )
                        )
                    )
                ])
            ]),
            html.Div([
                html.H6(
                    'Does the submission above contain gene names or uniprot codes?',
                    style={
                        'marginTop':'16px',
                        'marginLeft':'11px'
                    }
                ),
                dcc.Dropdown(
                    id='gene_or_uniprot',
                    options=[
                        {'label':'Gene Names', 'value':'gn'},
                        {'label':'Uniprot Codes', 'value': 'uid'}
                        
                    ],
                    value='gn',
                    style={
                        'marginLeft':'11px',
                        'width':'45%'
                    }
                )
            ]),
            html.Div([
                # Choosing signature dimesnionality (bootstraps and parallel only appear if 3D is chosen 
                html.H6(
                    'Select whether you would like a 2D or 3D signature',
                    style={
                        'marginTop':'11px',
                        'marginLeft':'11px'
                    }
                ),
                dcc.Dropdown(
                    id='dimension',
                    options=[
                        {'label':'2D', 'value':'2d'},
                        {'label':'3D', 'value': '3d'}
                    ],
                    value='2d',
                    style={
                        'marginLeft':'11px',
                        'width':'45%'
                    }
                ),
                html.H6(
                    'Select the number of bootstraps (the maximum number is 100)',
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
                    max=100,
                    style={
                        'display':'none',
                        'width':'35%'
                    }
                ),
                html.H6(
                    'Select the number of parallel processes (the maximum number is 2)',
                    id='para_process_label',
                    style={
                        'display':'none'
                    }
                ),
                dcc.Input(
                    id='n_para_process',
                    placeholder='Enter a number between 0 and 2...',
                    type='number',
                    min=0,
                    max=2,
                    style={
                        'display':'none',
                        'width':'35%'
                    }
                )
            ]),
            html.Div([
                # Input name of job (filename to export to)
                html.H6(
                    'Submit the name of the job (the filename the job will be exported to)',
                    style={
                        'margin':'11px',
                        'marginTop':'27px'
                    }
                ),
                dcc.Input(
                    id='output_name',
                    value=''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]),
                    style={
                        'marginLeft':'11px',
                        'width':'35%'
                    }
                )
            ]),
            html.Div([
                # Submit button
                html.Hr(),
                html.A(
                    html.Button(
                        'Submit',
                        id='submit_button',
                        style={
                            'marginLeft':'43%',
                            'marginRight':'43%'
                        }
                    ),
                    id='page_link'
                )
            ]),
            html.Div(
                # Structural signatures output to return to user
                id='struct_sig_output',
                style={
                    'marginLeft':'11px',
                    'marginTop':'27px',
                    'color': '#ea0202'
                }
            ),
            html.Div([
                #footer so I dont hit undo at bottom of page
                html.Hr(),
                html.Hr()
            ]),
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

# Shows filename and 'select different file' button when file selected, hides file selection box
@app.callback(
    [Output('upload_data_dragdrop', 'style'),
     Output('file_name_display', 'style'),
     Output('file_name_display', 'children'),
     Output('file_change_select', 'style')],
    [Input('upload_data_dragdrop', 'filename')]
    )

def update_filename_display(filename):
    file_change_select_dict = {
        'width': '95%',
        'height': '65px',
        'lineHeight': '65px',
        'borderWidth': '1px',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '11px',
    }
    file_name_display_dict={
        'width': '95%',
        'height': '65px',
        'lineHeight': '65px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '11px',
    }
    upload_data_dragdrop_dict={
        'width': '95%',
        'height': '150px',
        'lineHeight': '150px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '11px',                    
    } 
    if filename != None:
        return [
            {'display':'none'},
            file_name_display_dict,
            'Selected File: ' + filename,
            file_change_select_dict
        ]
    return [
        upload_data_dragdrop_dict,
        {'display':'none'},
        'None',
        {'display':'none'}
    ]

# Allows user to select a different file by pressing 'select different file' button (Takes them back to the drag drop box)
@app.callback(
    Output('upload_data_dragdrop', 'filename'),
    [Input('file_change_select', 'n_clicks')]
)

def choose_diff_file(n_clicks):
    return None

# Sets up link to be used when submit button is pressed
@app.callback(
    Output('page_link','href'),
    [Input('upload_data_dragdrop', 'filename'),
     Input('upload_data_dragdrop', 'contents'),
     Input('upload_data_paste', 'value'),
     Input('dimension', 'value'),
     Input('n_bootstraps', 'value'),
     Input('n_para_process', 'value'),
     Input('output_name', 'value')]
    )

def link_prep(filename, file_contents, gene_list, val_dimension, num_bootstraps, num_para_process, name_file_out):
    # Checks if inputs are valid
    test_inputs = input_valid(filename, file_contents, gene_list, val_dimension, num_bootstraps, num_para_process)
    
    if test_inputs == True:
        return '/apps/app2/' + name_file_out
    return None
    
# Runs structural signatures in response to 'Submit' button press
@app.callback(
    Output('struct_sig_output','children'),
    [Input('submit_button', 'n_clicks')],
    [State('upload_data_dragdrop', 'filename'),
     State('upload_data_dragdrop', 'contents'),
     State('upload_data_paste', 'value'),
     State('gene_or_uniprot', 'value'),
     State('dimension', 'value'),
     State('n_bootstraps', 'value'),
     State('n_para_process', 'value'),
     State('output_name', 'value'),
     ]
    )

def update_output(n_clicks, filename, file_contents, gene_list, id_type, val_dimension, num_bootstraps, num_para_process, name_file_out):
    if n_clicks == None:
        return None

    # Checks if inputs are valid
    test_inputs = input_valid(filename, file_contents, gene_list, val_dimension, num_bootstraps, num_para_process)

    # if inputs are not valid, shows error message and waits for correct inputs
    if test_inputs != True:
        return test_inputs

    # if inputs are valid proceed with running structural signatures
    
    # generates a file to input to structural sig (combines the input file and gene list if both exist)
    local_gene_file = './generated_files/' + name_file_out + '_gene_list_file.txt'
    f = open(local_gene_file, 'w+')
    f.close()
    if filename:
        gene_file_from_file(file_contents, local_gene_file)
    if gene_list:
        gene_file_from_list(gene_list, local_gene_file)

    if name_file_out not in os.listdir('./generated_files/'):
        os.mkdir('./generated_files/'+ name_file_out +'/')

    path_file_out = './generated_files/' + name_file_out + '/' + name_file_out

    # run structural signatures and clean up local gene file afterward
    if val_dimension == '2d':
        input_str = "./bin/structural-signatures-2.0-master/structural-signatures-2.0.sh -i " + local_gene_file + " -t both -n " + id_type + " -o " + path_file_out  
    else:
        input_str = "./bin/structural-signatures-2.0-master/structural-signatures-2.0.sh -i " + local_gene_file + " -t both -n " + id_type + " -o " + path_file_out + " -b " + str(num_bootstraps) + " -p " + str(num_para_process)
    struct_sig_sucess = subprocess.call(input_str, shell=True)
    os.remove(local_gene_file)

    # makes file containing whether structural signatures ran sucessfully or not
    struct_sig_sucess_file = './generated_files/' + name_file_out + '_struct_sig_sucess.txt'
    f = open(struct_sig_sucess_file, 'w+')
    f.write(str(struct_sig_sucess))
    f.close()
    # 0 if sucessfull
    return struct_sig_sucess

