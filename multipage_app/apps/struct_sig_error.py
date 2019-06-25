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
    html.Div([
        # Error message
        html.H6(
            'Error: There was an error in the generation of the structural signatures. Please check that your inputs are valid and resubmit',
            style={
                'textAlign': 'center',
                'marginTop': '27px'
            }
        ),
        # Button that links back to input page in response to structural signatures error
        html.A(
            html.Button(
                'Back to Input Page',
                id='back_to_input_button',
                style={
                    'marginLeft':'35%',
                    'marginRight':'35%',
                    'marginTop': '11px'
                }
            ),
            href='/apps'
        )
    ]),
    # Dummy variable to take output of callback
    html.Div(
        id='error_output'
    )
])

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

    