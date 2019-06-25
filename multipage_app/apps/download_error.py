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
                            html.Li(html.I(id='search',  className='fa fa-users')),
                            html.Li(html.A('About', href='/apps/about')), 
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
    # Error message
    html.H6(
        'Error: Too many days have elapsed, the files you are trying to acess have been removed',
        style={
            'textAlign': 'center',
            'marginTop': '27px'
        }
    )
])
