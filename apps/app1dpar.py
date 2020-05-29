print('in app1dpar')
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from parabolic1d_implicit import parab1dimp
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
print('imported dependencies')
print('import navbar')
from navbar import navbar
print('import helpers')
from helpers import render_slider
print('import app')
from app import app, server
print('imported everything for app1dpar')

initial_condition_labels = {#label:[min,max,symbol,unit]
    'uox1d_per':[5,90,'u(x=x,t=0)','%'],
    'ui':[200,800,'u(x=0,t=t)','K'],
    'cond1d':[.5,1.5,'k','W/Km']
    }
grid_setup_labels = {
    'xlength':[20,100,'X','m'],
    'xsteps':[5,55,'X steps',''],
    'tspan':[20,90,'%'+'ui','%'],
    'tsteps':[.5,1.5,'delt','s']
}

print('made it past slide settings in app1dpar')
#initla simulation based on default parm settings
parms = [(value[0]+value[1])/2 for key,value in initial_condition_labels.items()]+[
    (value[0]+value[1])/2 for key,value in grid_setup_labels.items()]
print('made it past parms list')
uox1d_per,ui,cond1d,xlength,xsteps,tspan,tstep = parms
print('made it past assign parms')
try:
    xgrid,ugrid = parab1dimp(xlength=xlength,delt=tstep,n=xsteps,uo_per=uox1d_per/100,uto=ui,ufper=tspan/100,k=cond1d)
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst) 
    xgrid = np.linspace(1,10)
    ugrid = xgrid
    

print('made it past set up in 1dpar')

def render_line_graph(xgrid,ugrid,tstep):
    #break the simulation output into 20 steps
    tframes = list(range(0,len(ugrid[:,0]),int(len(ugrid[:,0])/20)))
    figure = go.Figure(
        data = go.Scatter(
            #tframes = list(range(0,len(ugrid[:,0]),len(ugrid[:,0])/20))
            x=xgrid,y=ugrid[0,:],
            mode='lines+markers'
            
            #colorbar=dict(
                #   title='Temp. (K)'
                #  )
            ),
        layout = go.Layout(
            template="plotly_dark",
            margin= dict(l=40, r=10, b=40, t=10),
            xaxis_title="X (m)",
            yaxis_title="Temp. (K)",
            yaxis = dict(rangemode = 'tozero')
            ),
        #animation frames
        frames = [go.Frame(data=[go.Scatter(x=xgrid,y=ugrid[tframe,:])],name=str(t)) for t,tframe in enumerate(tframes)]
    )
    #Play and pause button 
    ###using gapminder example as template https://plotly.com/python/v3/gapminder-example/
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
    #Generate slider steps
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
        'label': '{seconds}'.format(seconds=round(tframe*tstep,2)),
        'method':'animate'
    } for t,tframe in enumerate(tframes)
    ]
    #Slider formatting
    sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 14},
        'prefix': 'Seconds:',
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

print('made it past render line graph')
layout = dbc.Container([
    navbar,
    #heading row
    dbc.Row([ 
        dbc.Col([
            html.H3('1D Parabolic Heat Equation')
        ],md=6,sm=12),
        dbc.Col([
            html.H3('\u2202q/\u2202t = -k\u2202\u00B2u/\u2202x\u00B2')
        ],md=6,sm=12)
    ]),
    #container for graph col and input cols
    dbc.Row([ 
        #graph column
        dbc.Col([ 
            dcc.Graph(figure=render_line_graph(xgrid,ugrid,tstep) ,id='parabolic1d-graph')
        ],sm=12,md=6),
        #Parameters
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

print('made it past layout')
#Call back to update the slider label with the slider value (since sliders have no tick labels)
for slider in [key+'-slider' for key in initial_condition_labels.keys()] + [key+'-slider' for key in grid_setup_labels.keys()]:
    @app.callback(
        Output('{slider}-output-container'.format(slider=slider),'children'),
        [Input(slider,'value')]
    )
    def update_output(value):
        return value

#Call back to rerun the simulation with the slider inputs
@app.callback(
    Output('parabolic1d-graph','figure'),
    [Input(key+'-slider','value') for key in initial_condition_labels.keys()]+
    [Input(key+'-slider','value') for key in grid_setup_labels.keys()]

)
def update_figure(uox1d_per,ui,cond1d,xlength,xsteps,tspan,tstep):
    #parab1dimp(xlength,delt,n,uo,uto,ufper,k)
    #print("initiate solver")
    xgrid,ugrid = parab1dimp(xlength=xlength,delt=tstep,n=xsteps,uo_per=uox1d_per/100,uto=ui,ufper=tspan/100,k=cond1d)
    #print("solver finished")
    return render_line_graph(xgrid,ugrid,tstep) 
    
print('made it past callbacks in app1dpar')