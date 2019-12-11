#################
# App Description
'''
This page checks if structural signatures ran correctly and sends the user to 
either the download page (download_page.py) or the error pages (struct_sig_error.py or download_error)
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
import glob
from app import app
import base64

#Style
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
    # Headding for page
    html.H3(
        'Calculating Structural Signatures...',
        style={
            'textAlign': 'center',
            'margin-top': 200,
            'margin-bottom':30,
            'color': theme_color3
        }
    ),
    html.H6(
        'This could take a few minutes, please be patient',
        style={
            'textAlign': 'center',
            'margin-bottom': 200
        }
    ),
    html.Div(
        children=None,
        id='path_prefix',
        style={
            'display':'none'
        }
    ),
    html.Div(children=[
        html.Center(children=[
            html.H6('Brought to you by the Schlessinger Lab. To find out more about the work that we do check out the ',
                style={
                    'display': 'inline-block',
                    'color': theme_color5,
                    # 'margin-left':100,
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
    ),
    # allows the app to check output after a preset amount of time 
    dcc.Interval(
        id='interval_component',
        # in milliseconds
        interval=1000*30,
        n_intervals=0
    ),
],
style={'backgroundColor':theme_color4})

################
# Callbacks

# Saves the value of the file name prefix that was saved as part of the url
@app.callback(
    Output('path_prefix', 'children'),
    [Input('interval_component', 'n_intervals')],
    [State('url', 'pathname')]
)
def get_file_prefix(num_intervals, pathname):
    return pathname[pathname.rfind('/')+1:]

# Checks the ouput and routs back to input page (app1)(if calculating error), no files page (app5)(if no files), or to results page (app3)(if no error)
@app.callback(
     Output('url', 'pathname'),
    [Input('interval_component', 'n_intervals'),
    Input('path_prefix', 'children')],
)

def check_output(num_intervals, file_prefix):
    temp_file = file_prefix + '_gene_list_file.txt'
    struct_sig_sucess =  file_prefix + '_struct_sig_sucess.txt'
    if temp_file not in os.listdir('./generated_files'):
        if struct_sig_sucess in os.listdir('./generated_files'):
            f = open('./generated_files/' + struct_sig_sucess, 'r')
            first_line = f.readline()
            f.close()
            if first_line == str(0):
                return '/apps/app3/'+ file_prefix
            return '/apps/app4/'+ file_prefix
        return '/apps/app5/'
    return '/apps/app2/' + file_prefix