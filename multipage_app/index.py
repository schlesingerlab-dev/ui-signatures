#################
# App Description
'''
This page is the skeleton for the entire app, run this to start the app
The first page the user sees when you run this is app1
'''

################
#Imports/Set UP

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from apps import app1, app2, app3, app4, app5

#################
# App Layout

app.layout = html.Div([
    dcc.Location(
        id='url', 
        refresh=False,
    ),
    html.Div(id='page-content')
])

################
# Callbacks

# Controls the page layout displayed based on the url pathname input
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/apps/app1' or pathname ==  '/' or pathname == '/apps' or pathname == None:
        return app1.layout
    elif len(pathname) >= 10:
        part_of_path = pathname[:10]
        if part_of_path == '/apps/app2':
            return app2.layout
        elif part_of_path == '/apps/app3':
            return app3.layout
        elif part_of_path == '/apps/app5':
            return app5.layout
    return app4.layout

################
# Running

if __name__ == '__main__':
    app.run_server(debug=True)