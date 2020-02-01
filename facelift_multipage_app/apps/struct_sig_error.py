#################
# App Description
'''
This is the error response page for structural signatures (not input problems)
It sends the user back to the input page (gene_input.py) if they click the back link
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import glob
import os
from app import app
import shutil
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
    html.Div([
        # Error message
        html.H1(
            'Error: There was an error in the generation of the structural signatures. Please check that your inputs are valid and resubmit',
            style={
                'textAlign': 'center',
                'margin-top': 150,
                'margin-left':70,
                'margin-right':70,
                'color': theme_color3
            }
        ),
        # Button that links back to input page in response to structural signatures error
        html.Center(
        html.A(
            html.Button(
                'Back to Input Page',
                id='back_to_input_button',
                style={
                    'margin-top': 50,
                    'margin-bottom': 150
                }
            ),
            href='/apps'
        ))
    ]),
    # Dummy variable to take output of callback
    html.Div(
        id='error_output'
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
    'backgroundColor':theme_color4,
})

################
# Callbacks

# Deletes files if structural signatures had error
@app.callback(
    Output('error_output', 'children'),
    [Input('back_to_input_button', 'n_clicks')],
    [State('url', 'pathname')]
)

def delete_bad_struct_sig_files(n_clicks, pathname):
    if n_clicks == None:
        return None

    pathname = pathname[pathname.rfind('/')+1:]
    shutil.rmtree('./generated_files/' + pathname)
    os.remove('./generated_files/' + pathname + '_struct_sig_sucess.txt')

    