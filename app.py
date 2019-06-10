#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#################
#Functions

def gene_file_from_list(gene_list, name_paste_gene_file):
    '''
    Inputs:
        gene_list: (str) comma and/or separated string of gene names or uniprot IDs
        name_paste_gene_file: (str) refers to an already existing file
    
    Outputs:
        None, but makes a line separated file of genes

    Description:
        genereates a file of line separated genes from the gene_list without duplicate genes
    '''
    # f = open(name_paste_gene_file, 'r')
    # first_line = f.readline()
    # if first_line =='':
    #     new_file = True
    # else:
    #     new_file = False
    # print(new_file)
    # f.close()

    f = open(name_paste_gene_file, 'a')
    gene = ''

    # For duplicate check
    duplicates = set()

    # Generate file
    for index in range(len(gene_list)):
        if gene_list[index] == ' ' or gene_list[index] == ',':
            if len(gene) > 0 and gene not in duplicates:
                # if not new_file and index == 0:
                #     f.write('\n' + gene + '\n')
                # else:
                f.write(gene + '\n')
                duplicates.add(gene)
            gene = ''
        else:
            gene += gene_list[index]
            if index == (len(gene_list)-1) and gene not in duplicates:
                # if not new_file and index == 0:
                #     f.write('\n' + gene + '\n')
                # else:
                f.write(gene + '\n')
                duplicates.add(gene)
                gene = ''
    f.close()

def gene_file_from_file(contents, name_local_file_from_file):
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
    if file_contents or gene_list:
        if file_contents:
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
                        html.Div(
                            className='row',
                            children=[
                                dcc.Upload(
                                    id='upload_data_dragdrop',
                                    children=html.Div([
                                            'Drag and Drop or ',
                                            html.A('Select File')
                                            ]),
                                    style={
                                        'width': '46%',
                                        'height': '150px',
                                        'lineHeight': '150px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px',
                                        'float': 'left',
                                        'display': 'none'
                                    } 
                                ),
                                html.Label(
                                    id='file_name_display',
                                    children='None',
                                    style={
                                        'width': '46%',
                                        'height': '65px',
                                        'lineHeight': '65px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
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
                                        'width':'46%',
                                        'height':'150px',
                                        'borderWidth': '1px',
                                        'borderRadius': '5px',
                                        'margin': '11px',
                                        'float': 'right'
                                    }
                                ),

                                html.Button(
                                    'Select different file',
                                    id='file_change_select',
                                    style={
                                        'width': '46%',
                                        'height': '65px',
                                        'lineHeight': '65px',
                                        'borderWidth': '1px',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px',
                                        'float': 'left'           
                                    }
                                )

                            ]
                        )
                ]),

                html.Div([
                    html.Label(
                        'Does the submission above contain uniprot codes or gene names?',
                        style={
                            'marginTop':'16px',
                            'marginLeft':'11px'
                        }
                    ),
                    dcc.RadioItems(
                            id='gene_or_uniprot',
                            options=[
                                {'label':'Uniprot Codes', 'value': 'uid'},
                                {'label':'Gene Names', 'value':'gn'}
                            ],
                            value='uid',
                            style={
                                'marginLeft':'11px'
                            }
                        )
                ]),


                # html.Div([
                #         #Choosing: fold, family, super family, and/or domain
                #         html.Label(
                #             'Select the output you would like from the server and then press the submit button',
                #             style={
                #                 'marginTop':'27px',
                #                 'marginLeft': '11px'
                #             }
                #          ),
                #         dcc.Checklist(
                #             id='divisions_to_use',
                #             options=[
                #                 {'label': 'Fold', 'value': 'fold'},
                #                 {'label': 'Family', 'value': 'family'},
                #                 {'label': 'Super Family', 'value': 'super_family'},
                #                 {'label': 'Domain', 'value': 'domain'},
                #                 {'label': 'All', 'value': 'all_divisions'}
                #              ],
                #             values=[],
                #             labelStyle={
                #                 'display':'inline-block',
                #                 'margin': '16px',
                #                 'marginLeft': '11px'
                #             }
                #          )
                # ]),
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
                            value='2d',
                            style={
                                'marginLeft':'11px'
                            }
                        ),
                        html.Label(
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
                        html.Label(
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

                # html.Div([
                #     # Allows selection of which version of Structural Signatures to use (FOR DEVELOPMENT PURPOSES)
                #     html.Label(
                #         'Select whether you would like to use version 1.0 or 2.0 of structural signatures (FOR DEVELOPMENT PURPOSES)',
                #         style={
                #            'margin':'11px',
                #            'marginTop':'27px' 
                #         }
                #     ),
                #     dcc.RadioItems(
                #         id='version_select',
                #         options=[
                #             {'label':'Version 1.0', 'value':'version1'},
                #             {'label':'Version 2.0', 'value': 'version2'}
                #         ],
                #         value='version2',
                #         style={
                #             'marginLeft':'11px'
                #         }
                #     ),
                # ]),
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
                        id='struct_sig_output',
                        style={
                           'marginLeft':'11px',
                            'marginTop':'27px'
                        }
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
        'width': '46%',
        'height': '65px',
        'lineHeight': '65px',
        'borderWidth': '1px',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'float': 'left'           
    }
    file_name_display_dict={
        'width': '46%',
        'height': '65px',
        'lineHeight': '65px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'float': 'left'
    }
    upload_data_dragdrop_dict={
        'width': '46%',
        'height': '150px',
        'lineHeight': '150px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'float': 'left',
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
     State('output_name', 'value')
#     State('version_select', 'value'),
#     State('divisions_to_use', 'values'),
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

    # # (FOR DEVELOPMENT) makes sure no gene names are input into version 1.0 of structural signatures
    # if ssversion == 'version1':
    #     if id_type == 'gene_name':
    #         return 'Gene Names are incompatible with Version 1.0. Please select Version 2.0 or select a different file'
    # # END OF DEV CODE 

    # Generate output file name if none given
    if name_file_out == None:
        name_file_out = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    
    # generates a file to input to structural sig (combines the input file and gene list if both exist)
    local_gene_file = 'gene_list_file_'+ name_file_out +'.txt'
    f = open(local_gene_file, 'w+')
    f.close()
    if filename:
        gene_file_from_file(file_contents, local_gene_file)
    if gene_list:
        gene_file_from_list(gene_list, local_gene_file)

    input_str = "./bin/structural-signatures-2.0.sh -i " + local_gene_file + " -t both -n " + id_type + " -o " + name_file_out
    subprocess.call(input_str, shell=True)

    #script_location= "bin/structural-signatures-2.0.sh"
    #input_args = ["./"+script_location, "-i", local_gene_file, "-t", "both", "-n", id_type, "o", name_file_out]
    #subprocess.Popen(input_args)
    
    #         os.remove(file)


 

if __name__ == '__main__':
    app.run_server(debug=True)
