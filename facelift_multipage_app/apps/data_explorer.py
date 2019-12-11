#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################
# App Description
'''
This page allows the user to explore the database 
'''

################
#Imports/Set UP

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import string
import random
import subprocess
import os
import urllib.parse
import dash_table
import pandas as pd
import plotly.graph_objs as go
from app import app

##############
# App style
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

tab_style = {'fontWeight': 'bold', 'color':theme_color5}
tab_selected_style = {'backgroundColor': theme_color5, 'fontWeight':'bold', 'color':theme_color1}
# load the databases
df_dict = {}
structure_types = ['domain', 'family', 'fold', 'superfam']

for structure in structure_types:
    edit_gtex = pd.read_csv('./bin/table_data_explorer/GTeX_ss/allcombined.250.' + structure + '.csv.3', 
    names=['Structure', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'FDR', 'Bonforroni', 'Log Fold Change', 'Sample ID', 'Subtissue', 'Organ'])
    edit_gtex = edit_gtex.drop(columns=['Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'Bonforroni', 'Log Fold Change', 'Sample ID'])
    df_dict['gtex_'+structure] = edit_gtex
    # split the last row of the archs data and adds it to the dictionary of databases
    edit_archs = pd.read_csv('./bin/table_data_explorer/ARCHS4_ss/allcombined.archs4.' + structure + '.csv',
        names=['Structure', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'FDR', 'Bonforroni', 'Log Fold Change', 'temp'])
    edit_archs[['Sample ID', 'Organ']] = edit_archs.temp.str.split('-',expand=True)
    edit_archs = edit_archs.drop(columns=['Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'Bonforroni', 'Log Fold Change','Sample ID', 'temp'])
    df_dict['archs_'+structure] = edit_archs

    df_dict['3Dgtex' + structure] = pd.read_csv('./bin/autoencoder_data/GTeX/tsne.' + structure + '.csv')
    df_dict['3Darchs' + structure] = pd.read_csv('./bin/autoencoder_data/archs/tsne.' + structure + '.archs.csv')
    


#################
#Functions

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

        html.Div(children=[
            html.H1('Explore', 
                style={
                    'color': theme_color3,
                    # 'padding-top': 50,
                    # 'padding_bottom': 50,
                    'margin-top': 50,
                    'display': 'table-cell'

                }),
            dcc.Dropdown(
                id='database_name',
                options=[
                    {'label':'gTEx', 'value':'gtex'},
                    {'label':'ARCHS', 'value': 'archs'} 
                ],
                value='gtex',
                style={
                    'margin-top': 25,
                    'margin-left':'11px',
                    'display': 'table',
                    # 'display': 'table-cell',
                    # 'height': 27,
                    # 'width':100,
                    'width': '55%'
                }
            ),
        ],
        style = {
                'width': '100%', 
                'display': 'flex', 
                'align-items': 'center', 
                'justify-content': 'center'
        }
        ),
    
    html.Center(
        html.H3('Select the database and level of classification to search',
            style={
                'color': theme_color1,
                'margin-left': 100,
                'margin-right': 100,
                'margin-top': 15,
                'padding-bottom': 50
                # 'margin-bottom': 30
            })
    ),
    # select the database to display data from
    html.Div([
        # show whether you want to see data for family, fold, superfamily, or domain
        dcc.Tabs(
            id='class_tabs',
            value='domain',
            vertical=False,
            children=[
                dcc.Tab(label='Domain', value='domain', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Fold', value='fold', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Family', value='family', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Superfamily', value='superfam', style=tab_style, selected_style=tab_selected_style)
            ],
            colors={
            # "border": theme_color1,
            "border": theme_color3,
            "background": theme_color1
            },
        ),
        # html.Center(
        #     html.H1('3D Visualization of Data Set', style={'color':theme_color5, 'margin-top':50})
        # ),
        # 3D graph of gene signatures and tissue types
        html.Div([dcc.Graph(id='3d_graph')],
            style={'margin-top':30}
        )
        ],
        style={
            'backgroundColor':theme_color5
        },
        ),
        
        html.Div([
        html.Center([
                html.H1('Search the ', style={'display':'inline-block', 'color': theme_color3, 'margin-top':50}),
                html.H1(id='disp_database', style={'display':'inline-block','margin-left':11, 'color': theme_color3}),
                html.H1(id='disp_class', style={'display':'inline-block', 'margin-left':11, 'color': theme_color3}),
                html.H1(' data table', style={'display':'inline-block', 'margin-left':11, 'color': theme_color3})
        ]),
        html.Div([
        # search table
        html.H3(
            'Search by:',
            style={
                'marginLeft':'50px',
                'marginTop': '30px',
                # 'marginBottom':'10px',
                'color': theme_color1,
                'display': 'inline-block',
                'vertical-align': 'middle'
            }
        ),
        dcc.Dropdown(
            id='search_type_gtex',
            options=[
                {'label':'Structure', 'value':'Structure'},
                # {'label':'Sample ID', 'value': 'Sample ID'},
                {'label':'Subtissue', 'value':'Subtissue'},
                {'label':'Organ', 'value':'Organ'}
                
            ],
            value='Structure',
        ),
        dcc.Dropdown(
            id='search_type_archs',
            options=[
                {'label':'Structure', 'value':'Structure'},
                # {'label':'Sample ID', 'value': 'Sample ID'},
                {'label':'Organ', 'value':'Organ'}
                
            ],
            value='Structure'
        )]),
        # Search table input
        dcc.Input(
            id='search_table',
            placeholder='Start typing to search...',
            style={
                'marginLeft':'50px',
                # 'marginBottom':'30px',
                'marginTop': 30,
                'width': 300,
                # 'display': 'inline-block',
                'vertical-align': 'middle',
            }
        ),
            ]),

            html.Center([
                # data table
                dash_table.DataTable(
                    id='database_display',
                    virtualization=True,
                    n_fixed_rows=1,
                    style_table={'overflowX': 'scroll', 
                    'maxWidth': '98%'
                    },
                    style_header={
                        # 'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        },
                    style_cell={
                        # 'minWidth': '0px', 'maxWidth': '50px',
                        'whiteSpace': 'normal',
                        'textAlign': 'center',
                        'font-family': 'sans-serif',
                    },
                    style_cell_conditional=[{
                            'if': {'column_id': 'Observed Counts'},
                            'minWidth': '50px'
                        }],
                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        # display: inline;
                        'rule': 'white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                ),
                ],
                style={'margin-bottom':30}
            ),
            html.Div([
                # shows if there is no data in the database
                html.Center(
                    html.H3(
                    id='database_error',
                    children='The value you searched for could not be found',
                    style={
                        'display':'none'
                    })
                )],
                
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
            )
],
style={
    'backgroundColor':theme_color4,
})


################
# Callbacks

@app.callback(
    [Output('search_type_gtex', 'style'),
     Output('search_type_archs', 'style')],
    [Input('database_name', 'value')]
)

def search_option_update(database_name):
    if database_name == 'gtex':
        return [{'vertical-align': 'middle','width':'45%', 'marginLeft':'15px','marginTop': '15px', 'display':'inline-block'}, {'display':'none'}]
    return [{'display':'none'}, {'vertical-align': 'middle','width':'45%', 'marginLeft':'15px','marginTop': '15px', 'display':'inline-block'}]

# displays searchable database table 
@app.callback(
    [Output('database_display', 'columns'),
     Output('database_display', 'data'),
     Output('disp_database', 'children'),
     Output('disp_class', 'children')],
    [Input('database_name', 'value'),
     Input('class_tabs', 'value'),
     Input('search_table', 'value')],
     [State('search_type_gtex', 'value'),
      State('search_type_archs', 'value')]
    )

def display_table(database_name, class_type, search_value, search_type_gtex, search_type_archs):
    if database_name == 'gtex':
        search_type_value = search_type_gtex
    else:
        search_type_value = search_type_archs

    df_all = df_dict[database_name + '_' + class_type]
    if search_value:
        df = df_all.loc[df_all[search_type_value].str.contains(search_value)]
    else:
        df = df_all.head(30)
        # df = df_all
    df = df.round(4)

    num_rows = len(df.index)
    for row in range(num_rows):
        organ_subtissue = df.iloc[row,3]
        organ = df.iloc[row,4]
        subtissue= organ_subtissue[len(organ)+1:]
        df.iloc[row,3]= subtissue
        
        # if class_type != 'domain':
        #     struct_change = df.iloc[row,0]
        #     df.iloc[row,0] = html.Td(html.A(struct_change, href='https://www.schlessingerlab.org/', target="_blank"))

    return[
        [{"name": i, "id": i} for i in df.columns],
        df.to_dict('records'),
        database_name,
        class_type
    ]

# database error if no data in the database to display
@app.callback(
    Output('database_error', 'style'),
    [Input('database_display', 'data')]
    )

def database_search_error(database_data):
    if database_data == []:
        return {'color':theme_color5}
    return {'display':'none'}

@app.callback(
    Output('3d_graph', 'figure'),
    [Input('database_name', 'value'),
     Input('class_tabs', 'value')]
)

def make_3d_graph(database_value, class_value):
    color_list = [theme_color2, '#c9b1c9', '#c97bc9', '#6b406b', '#ab2bab', 
    '#590e59', '#7a5991', '#682f8f','#d7a8ff', '#7200d6',
    '#41007a', '#006aff', '#92bffc', '#134fa1', '#57749c', 
    theme_color3, '#00bad6', '#006a7a', theme_color1, '#02f7f7',
    '#065c08', '#2e8a00', '#6c9159','#00ed27','#d0f799', 
    '#95ff00', '#587331', '#325203']

    color_index = 0
    df = df_dict['3D' + database_value + class_value]
    data_list = []
    # tissue_types = set(df['tissue'].tolist()[:20])
    tissue_types = sorted(set(df['tissue'].tolist()))
    for tissue in tissue_types:
        df_rows = df.loc[df['tissue'] == tissue]
        x_val = df_rows['V1']
        y_val = df_rows['V2']
        z_val = df_rows['V3']
        if database_value == 'gtex':
            tissue_val = df_rows['subtissue']
        else:
            tissue_val = df_rows['tissue']
        data_list.append(
            go.Scatter3d(
                x=x_val,
                y=y_val,
                z=z_val,
                text=tissue_val,
                mode='markers',
                marker={
                    'opacity': 0.8,
                    'color': color_list[color_index], 
                    'size': 6
                },
                name=tissue
            ))
        color_index += 1
    return {
        'data': data_list,
        'layout':{
                'title': '3D Visualization of Data Set',
                'titlefont': {'size':36, 'color': theme_color1},
                'scene': {
                    'xaxis': {'title':'tsne 1'},
                    'yaxis': {'title': 'tsne 2'}, 
                    'zaxis': {'title': 'tsne 3'},
                },
                'paper_bgcolor':'rgba(0,0,0,0)',
                'plot_bgcolor':'rgba(0,0,0,0)',
                'height': 800,
                'font': {'color':theme_color1}
        }
    }
