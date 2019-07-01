#################
# App Description
'''
This is the download page for the data from structural signatures, has a back button to gene_input.py
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import shutil
import glob
import pandas as pd
import math
import os
from flask import send_file
from zipfile import ZipFile
import random
import string
import dash_table
from app import app

download_session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])

#################
# Functions

def make_df_from_file(pathname, feature_type):
    '''
    Inputs:
        pathname: (str) filepath
        feature_type: (str) family, fold, superfamily, domain

    Outputs:
        df: (pandas dataframe) of the file read

    Description:
        takes info about which csv file and returns a dataframe of that csv
    '''
    pathname = pathname[pathname.rfind('/')+1:]
    df = pd.read_csv('./generated_files/' + pathname + '/' + pathname + feature_type)
    return df

def make_volcano(df):
    '''
    Inputs:
        df: (pandas dataframe) with headings (structure, counts_observed, background_counts, number_of_genes_in_set, total_number_proteins_proteome, pvalue, fdr, bonforroni_cutoff, log_fold_change, name)

    Outputs:
        (tupl) : the log fold change, the -log(p), bonferroni correction

    Description:
        gets the necesary parts for the volcano plot out of the dataframe
    '''
    x = df['log_fold_change'].tolist()
    text = df['structure'].tolist()
    bonferroni = df['bonforroni_cutoff'][0]
    y_pvalue = df['pvalue'].tolist()
    y = []
    for pval in y_pvalue:
        y.append(-math.log(pval))
    return (x,y,text,bonferroni)    

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
    # Hidden Div for storing session id
    html.Div(
        children=download_session_id,
        id='session_id',
        style={
            'display':'none'
        }
    ),
    # Page heading
    html.H3(
        'Download Results',
        style={
            'textAlign': 'center'
        }
    ),
    html.Hr(),
    # Download button label
    html.H6(
        'Click on the button below to download your results:',
        style={
            'marginLeft': '11px',
            'marginBottom': '16px',
            'textAlign': 'center'
        }
    ),
    # Download button
    html.A(
        'Download',
        id='download-zip',
        download = "example.zip",
        href="",
        target="_blank",
        n_clicks = 0,
        style={
            'height': '40px',
            'lineHeight': '40px',
            'width':'200px',
            'lineWidth':'70px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '11px',
            'marginLeft': '37%',
            'marginRight': '37%',
            'color': 'gray',
            'float': 'left' 
        }
	),
    # Number of days download link is valid message
    html.H6(
        'You will be able to access this personalized link to download your results at a later time for ZZZ days:',
        style={
            'marginLeft': '11px',
            'marginTop': '100px',
            'textAlign': 'center'
        }
    ),
    # Link to download
    html.H6(
        None,
        style={
            'textAlign': 'center',
            'marginTop': '11px',
            'marginBottom': '11px'
        },
        id='download_url'
    ),
    html.Hr(),
    # Graphs the user wants their data to be displayed as
    html.H3(
        'Visual Data Represenation',
        style={
            'textAlign' : 'center'
        }
    ),
    html.H6(
        'Select the graphs you would like to see displayed',
        style={
            'margin' : '11px'
        }
    ),
    dcc.Dropdown(
        id='graph_choice',
        options=[
            {'label': 'Volcano Plot', 'value': 'volcano'},
            # {'label': 'TBD', 'value': 'other_graph_options'}
        ],
        multi=True
    ),
    html.Div([
        dbc.Row([
            dbc.Col(
                # Volcano Plot
                dcc.Graph(
                    id = 'volcano_plot',
                    style={'display':'none'} 
                ),
            ),
            dbc.Col(
                # table of volcano plot info
                dash_table.DataTable(
                    id='display_volcano_structure',
                    virtualization=True,
                    style_table={'overflowX': 'scroll'},
                    style_cell={
                        'minWidth': '0px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                ),
            )
        ])
    ]),
    html.Hr(),
    html.Hr(),
    # Back to main page button
    dcc.Link(
        'Back',
        href='/apps/app1',
        style={
            'height': '40px',
            'lineHeight': '40px',
            'width':'70px',
            'lineWidth':'70px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '11px',
            'color': 'gray',
            'float': 'right'
        }
    )
])

################
# Callbacks

# displays the link to download files at a future time
@app.callback(
    Output('download_url', 'children'),
    [Input('url', 'href')]
)

def display_value(href):
    index = href.rfind('/')
    if index != -1:
        return href[:index-1] + '2' + href[index:]
    return href

# generates plots when dropdown values selected
@app.callback(
    [Output('volcano_plot', 'figure'),
     Output('volcano_plot', 'style')],
    [Input('graph_choice', 'value')],
    [State('url', 'pathname')]
)

def show_plot(type_graph, pathname):
    # make data frames of csv files
    df_domain = make_df_from_file(pathname, '-domain-enrichments.csv')
    df_family = make_df_from_file(pathname, '-family-enrichments.csv')
    df_fold = make_df_from_file(pathname, '-fold-enrichments.csv')
    df_superfam = make_df_from_file(pathname, '-superfam-enrichments.csv')

    # make volcano plots
    if 'volcano' in type_graph:
        # get values for volcano plot points
        x_domain, y_domain, text_domain, bonferroni_domain = make_volcano(df_domain)
        x_family, y_family, text_family, bonferroni_family = make_volcano(df_family)
        x_fold, y_fold, text_fold, bonferoni_fold = make_volcano(df_fold)
        x_superfam, y_superfam, text_superfam, bonferoni_superfam = make_volcano(df_superfam)
        all_x = set(x_domain + x_family + x_fold + x_superfam)
        x_min = min(all_x)
        x_max = max(all_x)
        max_bonferroni = max([bonferoni_fold, bonferoni_superfam, bonferroni_domain, bonferroni_family])


        # return points to plot
        return[{
            'data':[
                {
                'x': x_domain,
                'y': y_domain,
                'mode':'markers',
                'name':'Domain',
                'text':text_domain
                },
                {
                'x': x_family,
                'y': y_family,
                'mode':'markers',
                'name':'Family',
                'text':text_family   
                },
                {
                'x': x_fold,
                'y': y_fold,
                'mode':'markers',
                'name':'Fold',
                'text':text_fold   
                },
                {
                'x': x_superfam,
                'y': y_superfam,
                'mode':'markers',
                'name':'Super Family',
                'text':text_superfam   
                },
                {
                'x':[x_max],
                'y':[5],
                'name':'-log(p value) = 5',
                'mode':'lines',
                'line':
                    {'color': 'rgb(0, 0, 0)',
                     'width':2}
                },
                {
                'x':[x_max],
                'y':[max_bonferroni],
                'name':'Maximum Bonferroni Correction',
                'mode':'lines',
                'line':
                    {'color': 'rgb(128,128,128)',
                     'width':2}
                }
            ],
            'layout':{
                'title': 'Volcano Plot of Enrichments',
                'xaxis': {'title':'Logfold Change'},
                'yaxis': {'title': '-log(p value)'},
                'layout': {'clickmode': 'event+select'},
                'shapes':[
                {
                'type':'line',
                'x0':x_min - 0.5,
                'y0':5,
                'x1':x_max + 0.5,
                'y1':5,
                'line':
                    {'color': 'rgb(0, 0, 0)',
                     'width':2}
                },
                {
                'type':'line',
                'x0':x_min - 0.5,
                'y0':max_bonferroni,
                'x1':x_max + 0.5,
                'y1':max_bonferroni,
                'line':
                    {'color': 'rgb(128,128,128)',
                     'width':2}
                }
            ],
            }
        },
        {}
        ]

    return [{'data': [{'x': [], 'y': []}]}, {'display':'none'}]

# Display table of values from click and hover of volcano plot
@app.callback(
    [Output('display_volcano_structure','columns'),
     Output('display_volcano_structure', 'data')],
     [Input('volcano_plot', 'clickData'),
     Input('volcano_plot', 'hoverData')],
     [State('url', 'pathname')]
)

def display_volcano_table(clickData, hoverData, pathname):
    point_info_display = pd.DataFrame(columns=['ID', 'Description', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'FDR', 'Bonforroni', 'Log Fold Change'])
    points_to_display = []

    # make data frames of csv files
    df_domain = make_df_from_file(pathname, '-domain-enrichments.csv')
    df_family = make_df_from_file(pathname, '-family-enrichments.csv')
    df_fold = make_df_from_file(pathname, '-fold-enrichments.csv')
    df_superfam = make_df_from_file(pathname, '-superfam-enrichments.csv')
    parentchild_df = pd.read_csv('./bin/structural-signatures-2.0-master/bin/files/ParentChildTreeFile.txt', sep="\n", header=None, names=['row'])
    scop_df = pd.read_csv('./bin/structural-signatures-2.0-master/bin/files/scope_total_2.06-stable.txt', sep="|", header=None, names=['type', 'number', 'description'])

    if clickData:
        points_to_display += clickData['points']
    if hoverData:
        points_to_display += hoverData['points']
    
    for point in points_to_display:
        if point['curveNumber'] == 0:
            # use parent child doc for domain
            df_gen_data_row = df_domain.loc[df_domain['structure'] == point['text']]
            list_gen_data_row = df_gen_data_row.values.tolist()[0]
            df_row = parentchild_df.loc[parentchild_df['row'].str.contains(point['text'])]
            description_full = df_row['row'].values.tolist()
            if description_full != []:
                description = description_full[0][description_full[0].find('::')+2:-2]
                point_info_display = point_info_display.append(
                    {
                    'ID':point['text'], 
                    'Description':description,
                    'Observed Counts':list_gen_data_row[1], 
                    'Background Counts':list_gen_data_row[2], 
                    'Number of Genes':list_gen_data_row[3], 
                    'Total Number of Proteins':list_gen_data_row[4], 
                    'p value':list_gen_data_row[5], 
                    'FDR':list_gen_data_row[6], 
                    'Bonforroni':list_gen_data_row[7], 
                    'Log Fold Change':list_gen_data_row[8]
                    }, 
                    ignore_index=True)

        elif point['curveNumber'] != 4 and point['curveNumber'] != 5:
            #use scop total stable for family, fold, and superfamily
            df_row = scop_df.loc[scop_df['number'] == point['text']]
            description = df_row['description'].values.tolist()
            if point['curveNumber'] == 1:
                df_gen_data_row = df_family.loc[df_family['structure'] == point['text']]
            elif point['curveNumber'] == 2:
                df_gen_data_row = df_fold.loc[df_fold['structure'] == point['text']]
            elif point['curveNumber'] == 3:
                df_gen_data_row = df_superfam.loc[df_superfam['structure'] == point['text']]
            list_gen_data_row = df_gen_data_row.values.tolist()[0]
            if description != []:
                point_info_display = point_info_display.append(
                    {
                    'ID':point['text'], 
                    'Description':description,
                    'Observed Counts':list_gen_data_row[1], 
                    'Background Counts':list_gen_data_row[2], 
                    'Number of Genes':list_gen_data_row[3], 
                    'Total Number of Proteins':list_gen_data_row[4], 
                    'p value':list_gen_data_row[5], 
                    'FDR':list_gen_data_row[6], 
                    'Bonforroni':list_gen_data_row[7], 
                    'Log Fold Change':list_gen_data_row[8]
                    }, 
                    ignore_index=True)
    return [
        [{"name": i, "id": i} for i in point_info_display.columns],
        point_info_display.to_dict('records')
    ]

# Downloads files on click of button
@app.callback(
    Output('download-zip', 'href'),
    [Input('download-zip', 'n_clicks')],
    [State('url', 'pathname'),
     State('session_id', 'children')]
)

def generate_report_url(n_clicks, pathname, session_id_val):
    if n_clicks != 0:
        os.chdir('./generated_files')
        pathname = pathname[pathname.rfind('/')+1:]
        if session_id_val + '.zip' not in os.listdir('./'):
            zip_file = ZipFile('./' + session_id_val + '.zip', 'w')
            for file in os.listdir('./' + pathname):
                zip_file.write('./' + pathname + '/' + file)
        os.chdir('..')
    return '/dash/urldownload'

@app.server.route('/dash/urldownload')

def generate_download_url():
    return send_file('./generated_files/' + download_session_id + '.zip', attachment_filename = 'StructuralSignatures.zip', as_attachment = True)
