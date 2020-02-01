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
import base64

theme_color1 = '#223146'
theme_color2 = '#6C656C'
theme_color3 = '#94CFD8'
theme_color4 = '#788689'
theme_color5 = '#F0F3F3'

logo_small = 'static/logo_white_blue.png'
encoded_image = base64.b64encode(open(logo_small, 'rb').read())
logo_small_thumb = html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                'height' : 50,
                'margin': 10
            })

sinai = 'static/sinai_noback.png'
encoded_image = base64.b64encode(open(sinai, 'rb').read())
sinai_thumb = html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                # 'display': 'inline-block',
                'height' : 50,
                'margin': 10
            })

#################
# App Layout

layout = html.Div([
    html.Div(
        children=[
            #nav bar
            html.Nav(
                #inside div
                html.Div(
                    children=[
                        html.A(
                            logo_small_thumb,
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
                               html.Li(html.A('Generate Structural Signatures', href='/apps')), 
                            #    html.Li(html.I(id='search',  className='fa fa-users')),
                            #    html.Li(html.A('About', href='/apps/about')), 
                            ],
                            id='nav-mobile',
                            className='right hide-off-med-and-down',
                            style={'color': theme_color5}
                        ), 
                    ],
                    className='nav-wrapper'
                ),style={'background-color':theme_color1}),
        ],
        className='navbar-fixed'
    ),

    # Error message
    html.H1(
        'Error: Too many days have elapsed, the files you are trying to acess have been removed',
        style={
            'textAlign': 'center',
            'margin-top': 200,
            'color': theme_color3,
            'margin-bottom': 200,
            'margin-left':70,
            'margin-right':70
        }
    ),

    html.Div(children=[
        html.Center(children=[
            html.H6('Brought to you by the Schlessinger Lab. To find out more about the work that we do check out the ',
                style={
                    'display': 'inline-block',
                    'color': theme_color5,
                    'margin-top':30,
                    'margin-right':6
                }),
            html.A("Schlessinger Lab Website", href='https://www.schlessingerlab.org/', target="_blank", 
            style={'display': 'inline-block'}),
        ],
        ),
        html.Center(sinai_thumb)
    ],
    style= {'backgroundColor':theme_color1}
    )
],
style={
'background-color': theme_color4,
'*#scale':'width:150px; height:100px;'})
