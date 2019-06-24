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
from apps import home, gene_input, struct_sig_run_check, download_page, struct_sig_error, download_error

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
    if pathname ==  '/' or  pathname == None:
        return home.layout
    elif pathname == '/apps/app1' or pathname == '/apps':
        return gene_input.layout
    elif len(pathname) >= 10:
        part_of_path = pathname[:10]
        if part_of_path == '/apps/app2':
            return struct_sig_run_check.layout
        elif part_of_path == '/apps/app3':
            return download_page.layout
        elif part_of_path == '/apps/app5':
            return download_error.layout
    return struct_sig_error.layout

################
# Running

if __name__ == '__main__':
    app.run_server(debug=True)