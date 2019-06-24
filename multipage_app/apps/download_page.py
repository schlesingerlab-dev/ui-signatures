#################
# App Description
'''
This is the download page for the data from structural signatures
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
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
from app import app

download_session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])

#################
# Functions

def make_volcano(pathname, feature_type):
    pathname = pathname[pathname.rfind('/')+1:]
    df = pd.read_csv('./generated_files/' + pathname + '/' + pathname + feature_type)
    x = df['log_fold_change'].tolist()
    text = df['structure'].tolist()
    y_pvalue = df['pvalue'].tolist()
    y = []
    for pval in y_pvalue:
        y.append(-math.log(pval))
    return (x,y,text)
    

#################
# App Layout

layout = html.Div([
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
    html.Label(
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
    html.Label(
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
    html.Label(
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
    # Volcano Plot
    dcc.Graph(
        id = 'volcano_plot',
        style={'display':'none'} 
    ),
    html.Hr(),
    html.Div(id='test'),
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
    if 'volcano' in type_graph:
        x_domain, y_domain, text_domain = make_volcano(pathname, '-domain-enrichments.csv')
        x_family, y_family, text_family = make_volcano(pathname, '-family-enrichments.csv')
        x_fold, y_fold, text_fold = make_volcano(pathname, '-fold-enrichments.csv')
        x_superfam, y_superfam, text_superfam = make_volcano(pathname, '-superfam-enrichments.csv')
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
                }
            ],
            'layout':{
                'title': 'Volcano Plot of Enrichments',
                'xaxis': {'title':'Logfold Change'},
                'yaxis': {'title': '-log(p value)'},
                'layout': {'clickmode': 'event+select'}
            }
        },
        {}
        ]
    return [{'data': [{'x': [], 'y': []}]}, {'display':'none'}]

# # Displays structure corresponding to the point selected on the volcano plot
# @app.callback(
#     Output('display_volcano_click', 'children'),
#     [Input('volcano_plot', 'clickData')]
# )

# def display_volcano_struct(clickData):
#     if clickData == None:
#         return None
#     for point in clickData['points']:
#         if point['curveNumber'] == 0:
#             pass
#             # use parent child doc
#         else:
#             pass
#             #use scop total stable 
#     return len(clickData['points'])

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
