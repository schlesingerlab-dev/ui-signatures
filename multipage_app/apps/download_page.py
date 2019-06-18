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
from app import app

#################
# Functions

def make_volcano(pathname):
    pathname = pathname[pathname.rfind('/')+1:]
    df = pd.read_csv('./generated_files/' + pathname + '/' + pathname + '-domain-enrichments.csv')
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
        x,y,text = make_volcano(pathname)
        return[{
            'data':[{
                'x': x,
                'y': y,
                'mode':'markers',
                'text':text
            }],
            'layout':{
                'title': 'Volcano Plot of Domain Enrichments',
                'xaxis': {'title':'Logfold Change'},
                'yaxis': {'title': '-log(p value)'},
            }
        },
        {}
        ]
    return [{'data': [{'x': [], 'y': []}]}, {'display':'none'}]

# Downloads files on click of button
@app.callback(
    Output('download-zip', 'href'),
    [Input('download-zip', 'n_clicks')],
    [State('url', 'pathname')]
)

def generate_report_url(n_clicks, pathname):
    os.chdir('./generated_files')
    pathname = pathname[pathname.rfind('/')+1:]
    if 'StructuralSignatures.zip' not in os.listdir('./' + pathname):
        zip_file = ZipFile('./' + pathname + '/StructuralSignatures.zip', 'w')
        for file in os.listdir('./' + pathname):
            if file != 'StructuralSignatures.zip':
                zip_file.write('./' + pathname + '/' + file)
    os.chdir('..')
    return '/dash/urldownload'

@app.server.route('/dash/urldownload')

def generate_download_url():
    return send_file('./generated_files/OUT/StructuralSignatures.zip', attachment_filename = 'StructuralSignatures.zip', as_attachment = True)
