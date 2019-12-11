#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################
# App Description
'''
This page takes user input for structural signatures
checks if there is input, 
and sends user to 'calculating page' (struct_sig_run_check.py) 
'''

################
#Imports/Set UP

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State 
import dash_dangerously_set_inner_html as dash_html
import base64
import string
import random
import subprocess
import os
import urllib.parse
from app import app
import pandas as pd
import plotly.graph_objs as go

#################
# App Style

# external css 
#define the external urls
external_css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({'external_url': css})

external_js = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.js"]
for js in external_js:
  app.scripts.append_script({'external_url': js})

app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})

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

logo_big = 'static/logo_blue_gray_noback.png'
encoded_image = base64.b64encode(open(logo_big, 'rb').read())
logo_big_thumb = html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                # 'height' : 50,
                'margin': 10
            })

figure1_round = 'static/figure_oval.png'
encoded_image = base64.b64encode(open(figure1_round, 'rb').read())
figure1_thumb = html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                # 'height' : 350,
                'margin': 75
            })

figure2 = 'static/heart.png'
encoded_image = base64.b64encode(open(figure2, 'rb').read())
figure2_thumb = html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                'height' : 350,
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

################
# Functions

# load the databases
df_dict = {}
structure_types = ['domain', 'family', 'fold', 'superfam']

for structure in structure_types:
    edit_gtex = pd.read_csv('./bin/table_data_explorer/GTeX_ss/allcombined.250.' + structure + '.csv.3', 
    names=['Structure', 'Observed Counts', 'Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'FDR', 'Bonforroni', 'Log Fold Change', 'Sample ID', 'Subtissue', 'Organ'])
    edit_gtex = edit_gtex.drop(columns=['Background Counts', 'Number of Genes', 'Total Number of Proteins', 'p value', 'Bonforroni', 'Log Fold Change', 'Sample ID'])
    df_dict['gtex_'+structure] = edit_gtex

    df_dict['3Dgtex' + structure] = pd.read_csv('./bin/autoencoder_data/GTeX/tsne.' + structure + '.csv')
    

def make_3d_graph(class_value):
    color_list = [theme_color2, '#c9b1c9', '#c97bc9', '#6b406b', '#ab2bab', 
    '#590e59', '#7a5991', '#682f8f','#d7a8ff', '#7200d6',
    '#41007a', '#006aff', '#92bffc', '#134fa1', '#57749c', 
    theme_color3, '#00bad6', '#006a7a', theme_color5, '#02f7f7',
    '#065c08', '#2e8a00', '#6c9159','#00ed27','#d0f799', 
    '#95ff00', '#587331', '#325203']
    color_index = 0
    df = df_dict['3Dgtex' + class_value]
    data_list = []
    tissue_types = set(df['tissue'].tolist())
    for tissue in tissue_types:
        df_rows = df.loc[df['tissue'] == tissue]
        x_val = df_rows['V1']
        y_val = df_rows['V2']
        z_val = df_rows['V3']
        tissue_val = df_rows['subtissue']
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
                'title': 't-SNE Domain Enrichment',
                'titlefont': {'size':36, 'color': theme_color3},
                'scene': {
                    'xaxis': {'title':'tsne 1'},
                    'yaxis': {'title': 'tsne 2'}, 
                    'zaxis': {'title': 'tsne 3'},
                },
                'paper_bgcolor':'rgba(0,0,0,0)',
                'plot_bgcolor':'rgba(0,0,0,0)',
                'height': 800,
                'font': {'color':theme_color1}
                # "plot_bgcolor": "rgb(182, 215, 168)"
        }
    }

domain_fig = make_3d_graph('domain')

#################
# App Layout

layout = html.Div( id='main-page-content',children= [
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
    html.Div(children =[
        # html.Center(children=[
        #     logo_big_thumb,
        #     html.H3('A database to explore enriched structures in overexpressed and differentially expressed genes',
        #     style={
        #         'color': theme_color1,
        #         # 'margin-left': 100,
        #         # 'margin-right': 100,
        #         # 'padding-bottom': 100,
        #         # 'margin-bottom': 30
        #     })
        # ],
        # # style={'background-image': 'url("static/back_squares.png")'}
        # style={'background-image': 'url("static/back_squares_small1.png")'}
        # ),
        html.Div(children=[
            html.Center(children=[
                logo_big_thumb,
                html.H3('A database to explore enriched structures in overexpressed and differentially expressed genes',
                style={
                'color': theme_color1,
                'margin-left': 100,
                'margin-right': 100,
                # 'padding-bottom': 100,
                'margin-top': 30,
                'margin-bottom': 60
                })]
            )
        ],
        style={
            'padding': '50px 10px 10px',
            'box-shadow': '5px 5px 5px #6C656C',
            'background-image': 'url("static/back_squares_small1.png")'
            }
        ),
        html.Div(children=[
            html.Center(children=[
                html.H2('What are structural signatures?'),
                html.H5('Structural signatures are protein domains, families, superfamilies and folds that describe sets of overexpressed and differntially expressed genes. We utilize Interproscan to assign protein domains and SCOPe to assign protein families, superfamilies and folds. The count of each structural feature is recorded and compared to the proteome to compute p values, q values, and log10 fold changes.', 
                style={'padding-top': 50}),
                # html.A('Interproscan', href='http://www.ebi.ac.uk/Tools/services/web/toolform.ebi?tool=iprscan5&sequence=uniprot:KPYM_HUMAN', target='_blank'),
                # html.H5('to assign protein domains and'),
                # html.A('SCOPe', href='(http://scop.berkeley.edu/', target='_blank'),
                # html.H5('to assign protein families, superfamilies and folds.'),
                # figure1_thumb
            ],
            style={'color':theme_color5,
            'padding-left':100,
            'padding-right': 100}
            ),
            html.Center(children=[figure1_thumb])],
            style={
            # 'backgroundColor':theme_color3,
            'padding': '50px 10px 10px',
            'box-shadow': '5px 5px 5px #6C656C',
            'background-image': 'url("static/back.png")'
            # 'background-image': 'url("static/giphy.gif")'
            }
            ),

        html.Div(children=[
            html.Center(children=[
                html.H2('Why use structural signatures?'),
                html.H5("Between RNA-sequencing experiments, the expression of specific genes can change due to a variety of reasons, such as changes in protcol, laboratory techninque, reference geneome alignment. While an individual gene's expression may vary,  the represention of structural properties of a set of genes (such as protein domains) are more resliant to change.", 
                style={'padding-top': 50}),
                html.H5("As a result, we argue that structural enrichment offers a robust signature for comparing gene expression changes between RNA sequencing experiments. Strucutral enrichment also retains information present in the gene level as well.", 
                style={'padding-top': 25, 'padding-bottom':25}),
            ],
            style={'color':theme_color1,
            'padding-left':100,
            'padding-right': 100}
            ),
            html.Center(children=[
                figure2_thumb,
                html.H6('Pairwise jaccard coefficients between GTeX heart tissues across the top 250 genes and domain, family superfamily and fold enrichments',
                style={'color':theme_color1,
                'margin-bottom':60,
                'margin-top':25}
                )])
            ],
            style={
            # 'backgroundColor':theme_color3,
            'padding': '50px 10px 10px',
            'box-shadow': '5px 5px 5px #6C656C',
            'background-image': 'url("static/test_back.png")'
            }
            ),
            html.Div(children=[
                dcc.Graph(id='domain_graph', figure=domain_fig),
                # html.Center(html.H6('t-SNE projects of A) the top 250 overexpressed genes from GTeX, B) domain enrichment c) Fold enrichment.'))
            ],
            style={'padding-top': 50}
            # style= {
            #     'height' : 1200, 
            #     'width' : 1200
            # }
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
        # 'border': 'grey',
        '*#scale':'width:150px; height:100px;', 
        # 'padding': '6px 0px 0px 8px'
        })
])



