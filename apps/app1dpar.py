


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from parabolic1d_implicit import parab1dimp
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
    'tspan':[20,90,'%'+'ui','%'],
    'tsteps':[.1,2,'delt','s']
}

def render_line_graph(xgrid,ugrid):
    #print(ugrid.shape)
    tframes = list(range(0,len(ugrid[:,0]),int(len(ugrid[:,0])/20)))
    figure = go.Figure(
        data = go.Scatter(
            #tframes = list(range(0,len(ugrid[:,0]),len(ugrid[:,0])/20))
            x=xgrid,y=ugrid[0,:]
            #colorbar=dict(
                #   title='Temp. (K)'
                #  )
            ),
        layout = go.Layout(
            template="plotly_dark",
            margin= dict(l=40, r=10, b=40, t=10),
            scene=dict(xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Temp. (K)"),
            ),
        frames = [go.Frame(data=[go.Scatter(x=xgrid,y=ugrid[tframe,:])],name=str(t)) for t,tframe in enumerate(tframes)]
    )

    figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 0, 'easing': 'linear'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
    ]
    steps = [
    {
        # 'method': 'animate',
        # 'label': '{t}'.format(t=t),
        # 'value': '{t}-name'.format(t=t),
        # 'args': [{'frame': {'duration': 300, 'redraw': False},
        #     'mode': 'immediate'}]
        'args':[
            [t],{'frame': {'duration':300,'redraw': False},'mode':'immediate','transition':{'duration':0}}
        ],
        'label': t,
        'method':'animate'
    } for t,tframe in enumerate(tframes)
    ]
    sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
    }
    sliders_dict['steps'] = steps
    figure['layout']['sliders'] = [sliders_dict]
    return figure

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
            # [dcc.Graph(
            #     figure=render_surfaceplot(xgrid=xgrid,ygrid=ygrid,ugrid=ugrid),id='elliptic-graph'
            #     )]
            dcc.Graph(figure=go.Figure(),id='parabolic1d-graph')
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


@app.callback(
    Output('parabolic1d-graph','figure'),
    [Input(key+'-slider','value') for key in initial_condition_labels.keys()]+
    [Input(key+'-slider','value') for key in grid_setup_labels.keys()]

)
def update_figure(uox1d,ui,cond1d,xlength,xsteps,tspan,tstep):
    #parab1dimp(xlength,delt,n,uo,uto,ufper,k)
    print("initiate solver")
    xgrid,ugrid = parab1dimp(xlength=xlength,delt=tstep,n=xsteps,uo=uox1d,uto=ui,ufper=tspan/100,k=cond1d)
    print("solver finished")
    return render_line_graph(xgrid,ugrid) 
    
# initial_condition_labels = {#label:[min,max,symbol,unit]
#     'uox1d':[200,800,'u(x=x,t=0)','K'],
#     'ui':[200,800,'u(x=0,t=t)','K'],
#     'cond1d':[.00001,.00101,'k','mW/K']
#     }
# grid_setup_labels = {
#     'xlength':[10,110,'X','m'],
#     'xsteps':[5,55,'delX','m'],
#     'tspan':[0,100,'%'+'ui','%'],
#     'tsteps':[5,55,'delt','s']
# for slider in ['uox-slider','ufx-slider','uoy-slider','ufy-slider','heatflux-slider','conductivity-slider']:
#     @app.callback(
#         Output('%s-output-container'%slider, 'children'),
#         [Input(slider, 'value')])
#     def update_output(value):
#         return value

