


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
#from parabolic1d_implicit import elliptic2dsolve
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from navbar import navbar
from helpers import render_slider
from app import app

initial_condition_labels = {#label:[min,max,symbol,unit]
    'uox1d':[200,800,'u(x=x,t=0)','K'],
    'ui':[200,800,'u(x=0,t=t)','K'],
    'cond1d':[.00001,.00101,'k','mW/K']
    }
grid_setup_labels = {
    'xlength':[10,110,'X','m'],
    'xsteps':[5,55,'delX','m'],
    'tspan':[0,100,'%'+'ui','%'],
    'tsteps':[5,55,'delt','s']
}

layout = dbc.Container([
    navbar,
    dbc.Row([ #heading row
        dbc.Col([
            html.H3('1D Parabolic Heat Equation')
        ],md=6,sm=12),
        dbc.Col([
            html.H3('dq/dt = -k\u2207\u00B2')
        ],md=6,sm=12)
    ]),
    dbc.Row([ #container for graph col and input cols
        dbc.Col([ #graph column
            'graph'
        ],sm=12,md=6),
        dbc.Col(
            [dbc.Row(dbc.Col([html.H5('Boundary Conditions & Parameters')],width=12))]
            +
            [render_slider(label=key,vmin=value[0],vmax=value[1],
                symbol=value[2],units=value[3]) for key, value in initial_condition_labels.items()]
            +[dbc.Row(dbc.Col([html.H5('Grid Set-up')],width=12))]
            +[render_slider(label=key,vmin=value[0],vmax=value[1],
                symbol=value[2],units=value[3]) for key, value in grid_setup_labels.items()]
            ,
            md=6,sm=12
        )
    ])
])


for slider in [key+'-slider' for key in initial_condition_labels.keys()] + [key+'-slider' for key in grid_setup_labels.keys()]:
    @app.callback(
        Output('{slider}-output-container'.format(slider=slider),'children'),
        [Input(slider,'value')]
    )
    def update_output(value):
        return value
# for slider in ['uox-slider','ufx-slider','uoy-slider','ufy-slider','heatflux-slider','conductivity-slider']:
#     @app.callback(
#         Output('%s-output-container'%slider, 'children'),
#         [Input(slider, 'value')])
#     def update_output(value):
#         return value

