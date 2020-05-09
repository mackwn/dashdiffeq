# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

#external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[500,500],[1000,500],.1,.0001,10,10)

slider_labels = {#label:[min,max,symbol,unit]
    'uox':[200,800,'u(x=0,y=y)','K'],
    'ufx':[200,800,'u(x=f,y=y)','K'],
    'uoy':[200,800,'u(x=x,y=0)','K'],
    'ufy':[200,800,'u(x=x,y=f)','K'],
    'heatflux':[0,1,'q','mW/m\u00B2'],
    'conductivity':[.00001,.00101,'k','mW/K']
}

def render_slider(label,vmin,vmax,symbol,units): 

    output = dbc.Row([
            dbc.Col(
                dbc.Badge([
                    '{symbol}: '.format(symbol=symbol),
                    html.Span(id='{label}-slider-output-container'.format(label=label)),
                    ' {units}'.format(units=units)
                ],color='primary',className='slider-labels'),
                width = 3
            ),
            dbc.Col(
                dcc.Slider(
                    id='{label}-slider'.format(label=label),
                    min = vmin,
                    max = vmax,
                    value = (vmin+vmax)/2,
                    step = (vmax-vmin)/10
                ),
                width = 9
            )
        ])
    return output 

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

app.layout = dbc.Container([
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
    xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[uoy,ufy],[uox,ufx],flux,conduc,10,10)

    return render_surfaceplot(xgrid,ygrid,ugrid)
    



if __name__ == '__main__':
    app.run_server(debug=True)