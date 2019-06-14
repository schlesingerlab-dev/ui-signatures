#################
# App Description
'''
This page checks if structural signatures ran correctly and sends the user to 
either the download page (app3) or the error page (app4)
'''

################
#Imports/Set UP
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
import glob
from app import app

#################
# App Layout

layout = html.Div([
    # Headding for page
    html.H3(
        'Calculating Structural Signatures...',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(
        children=None,
        id='path_prefix',
        style={
            'display':'none'
        }
    ),
    # allows the app to check output after a preset amount of time 
    dcc.Interval(
        id='interval_component',
        # in milliseconds
        interval=1000*30,
        n_intervals=0
    )
])

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