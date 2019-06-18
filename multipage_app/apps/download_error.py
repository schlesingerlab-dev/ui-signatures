#################
# App Description
'''
Displays error that user's files are not in the generated_files folder 
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import glob
import os
from app import app

#################
# App Layout

layout = html.Div([
    # Error message
    html.H6(
        'Error: Too many days have elapsed, the files you are trying to acess have been removed',
        style={
            'textAlign': 'center',
            'marginTop': '27px'
        }
    )
])
