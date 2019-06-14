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
from app import app

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
    html.Button(
        'Download',
        id='download_button',
        style={
            'width': '46%',
            'height': '65px',
            'lineHeight': '65px',
            'marginLeft':'28%',
            'marginRight':'28%'       
        }
    ),
    # Outcome of download message
    html.Label(
        'You have downloaded your results',
        id='success_download',
        style={
            'textColor': 'green',
            'textAlign': 'center',
            'margin': '11px',
            'display': 'none'
        }
    ),
    # Number of days download link is valid message
    html.Label(
        'You will be able to access this personalized link to download your results at a later time for ZZZ days:',
        style={
            'marginLeft': '11px',
            'marginTop': '50px',
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

# Downloads files on click of button (error message displayed if no files to download)
@app.callback(
    [Output('success_download', 'style'),
     Output('success_download', 'children')],
    [Input('download_button','n_clicks')],
    [State('url', 'pathname')]
)

def download_files(n_clicks, pathname):
    if n_clicks == None:
        return [
            {'display': 'none'},
            None
        ]

    pathname = pathname[pathname.rfind('/')+1:]
    files_to_copy = glob.glob('./generated_files/' + pathname + '*')
    
    if len(files_to_copy) == 0:
        return [
            {
            'color': '#ea0202',
            'textAlign': 'center',
            'margin': '11px'
            },
            'Your results are no longer available to download, too much time has elapsed'
        ]
    for file in files_to_copy:
        if file != './generated_files/' + pathname + '_struct_sig_sucess.txt':
            shutil.copy(file, '/Users/nicolezatorski/Downloads/', follow_symlinks=True)
    return [
        {
        'color': '#20c403',
        'textAlign': 'center',
        'margin': '11px'
        },
        'You have downloaded your results'
    ]
