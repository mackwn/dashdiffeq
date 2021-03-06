print('inside app2del')
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
print('imported dependencies')
print('import app')
from app import app
print('importing elliptic2d')
#from elliptic2d import elliptic2dsolve
from diffeq.elliptic import elliptic2d
print('import navbar')
from navbar import navbar
print('import helpers')
from helpers import render_slider
print('imported everything for app2del')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


ellp2d = elliptic2d(3,4,10,10,[500,500],[1000,500],.1,.0001)
ellp2d.setup()
ellp2d.solve()
xgrid, ygrid, ugrid = ellp2d.xgrid, ellp2d.ygrid, ellp2d.ugrid


slider_labels = {#label:[min,max,symbol,unit]
    'uox':[200,800,'u(x=0,y=y)','K'],
    'ufx':[200,800,'u(x=f,y=y)','K'],
    'uoy':[200,800,'u(x=x,y=0)','K'],
    'ufy':[200,800,'u(x=x,y=f)','K'],
    'heatflux':[0,1,'q','W/m\u00B2'],
    'conductivity':[.00001,.00101,'k','W/K']
}

 

def render_surfaceplot(xgrid,ygrid,ugrid):

    figure = go.Figure(
        data = go.Surface(
            x=xgrid,y=ygrid,z=ugrid,
            colorbar=dict(
                title='Temp. (K)'
                )
            ),
        layout = go.Layout(
            template="plotly_dark",
            margin= dict(l=40, r=10, b=40, t=10),
            scene=dict(xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Temp. (K)")
            )
    )
    return figure

layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col([
            html.H3('2D Elliptical Heat Equation')
        ],md=6,sm=12),
        dbc.Col([
            html.H3('q = -k\u2207\u00B2')
        ],md=6,sm=12)
    ]),
    dbc.Row([
        dbc.Col( #Graph 
            [dcc.Graph(
                figure=render_surfaceplot(xgrid=xgrid,ygrid=ygrid,ugrid=ugrid),id='elliptic-graph'
                )],
            md=6,sm=12
        ),
        dbc.Col([dbc.Row(dbc.Col([html.H5('Boundary Conditions & Parameters')],width=12))]+[
            render_slider(label=key,vmin=value[0],vmax=value[1],
                symbol=value[2],units=value[3]) for key, value in slider_labels.items() # rainbows
        ],
            md=6,sm=12
        )
    ])
])


for slider in ['uox-slider','ufx-slider','uoy-slider','ufy-slider','heatflux-slider','conductivity-slider']:
    @app.callback(
        Output('%s-output-container'%slider, 'children'),
        [Input(slider, 'value')])
    def update_output(value):
        return value

@app.callback(
    Output('elliptic-graph','figure'),
    [Input('uox-slider','value'),
    Input('ufx-slider','value'),
    Input('uoy-slider','value'),
    Input('ufy-slider','value'),
    Input('heatflux-slider','value'),
    Input('conductivity-slider','value'),
    
    ]
)
def update_figure(uox,ufx,uoy,ufy,flux,conduc):
    ellp2d = elliptic2d(3,4,10,10,[uoy,ufy],[uox,ufx],flux,conduc)
    ellp2d.setup()
    ellp2d.solve()

    return render_surfaceplot(ellp2d.xgrid, ellp2d.ygrid, ellp2d.ugrid)
    
print('made it out of app2del.py')