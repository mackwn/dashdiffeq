print('made it into about')
#import dash
import dash_core_components as dcc
import dash_html_components as html
#import numpy as np
#from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
#import plotly.graph_objects as go
from navbar import navbar
from app import app, server
print('imported everything for about')

layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col([
            html.H3('Interactive Heat Equations')
        ],md=6,sm=12),
        dbc.Col([
            html.H3('S MKwn 2020')
        ],md=6,sm=12)
    ])
])