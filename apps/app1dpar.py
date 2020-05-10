


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from navbar import navbar

from app import app

layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col([
            html.H3('1D Parabolic Heat Equation')
        ],md=6,sm=12),
        dbc.Col([
            html.H3('dq/dt = -k\u2207\u00B2')
        ],md=6,sm=12)
    ])
])