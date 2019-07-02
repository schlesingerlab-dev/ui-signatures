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

#################
# App Layout

# external css 

#define the external urls
external_css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]

for css in external_css:
    app.css.append_css({'external_url': css})

external_js = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.js"]

for js in external_js:
  app.scripts.append_script({'external_url': js})

app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})

layout = html.Div( id='main-page-content',children= [
    html.Div(
        children=[
            #nav bar
            html.Nav(
                #inside div
                html.Div(
                    children=[
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
                            #    html.Li(html.I(id='search',  className='fa fa-users')),
                            #    html.Li(html.A('About', href='/apps/about')), 
                            ],
                            id='nav-mobile',
                            className='right hide-off-med-and-down'
                        ), 
                    ],
                    className='nav-wrapper'
                ),style={'background-color':'#4c586f'}),
        ],
        className='navbar-fixed'
    ),
    html.Div(
        html.Center(
        dcc.Markdown('''

## Welcome to Structural Signatures! 


#### A database to explore enriched structures in overexpressed and differentially expressed genes. 

![](static/example3.png)

## What are structural signatures? 

##### Structural signatures are protein domains, families, superfamilies and folds that describe sets of overexpressed and differntially expressed genes.

##### We utilize [Interproscan](http://www.ebi.ac.uk/Tools/services/web/toolform.ebi?tool=iprscan5&sequence=uniprot:KPYM_HUMAN) to assign protein domains and [SCOPe](http://scop.berkeley.edu/) to assign protein families, superfamilies and folds. 

## Why use structural signatures?

##### Between RNA-sequencing experiments, the expression of specific genes can change due to a variety of reasons, such as changes in protcol, laboratory techninque, reference geneome alignment. While an individual gene's expression may vary,  the represention of structural properties of a set of genes (such as protein domains) are more resliant to change. 
##### As a result, we argue that structural enrichment offers a robust signature for comparing gene expression changes between RNA sequencing experiments. Strucutral enrichment also retains information present in the gene level as well. 
![](static/figure1.png)

**Figure 1:** Pairwise jaccard coefficients between GTeX Tissues across the top 250 genes and domain, family superfamily and fold enrichments. 

![](static/figure3.png)

**Figure 2:** t-SNE projects of A) the top 250 overexpressed genes from GTeX, B) domain enrichment c) Fold enrichment.  

#
    ''')  
    ) , style={
        # 'backgroundColor':'#f1f0ea',
        # 'border': 'grey',
        '*#scale':'width:150px; height:100px;', 
        'padding': '6px 0px 0px 8px'} )
])


################