# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[500,500],[1000,500],.1,.0001,10,10)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='Interactive 2D Heat Equation',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='q = -k\u2207\u00B2',
        style={
            'textAlign': 'center',
            'color': colors['text']
    }),


    html.Div([
    
    ##Div for graph
        html.Div([
            dcc.Graph(
                id='elliptic-graph',
                figure={
                    'data': [
                        {'z': ugrid, 'type': 'contour', 'name': 'SF','transpose':True,
                        'x':xgrid[:,0],'y':ygrid[0,:]
                        },
                    ],
                    'layout': {
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            )
        ],style={'width': '40%', 'display': 'inline-block', 'padding': '0 20'}),

    
        #Div for sliders
        html.Div([

        'u(x=0,y=y) - left side temperature',    
        dcc.Slider( #u(x=0,y=y)
            id='uox-slider',
            min=300,
            max=700,
            value=500,
            marks={temp: '%s K'%temp for temp in range(300,750,50)},
            step=None
        ), 
        'u(x=f,y=y) - right side temperature',
        dcc.Slider( #u(x=f,y=y)
            id='ufx-slider',
            min=300,
            max=700,
            value=500,
            marks={temp: '%s K'%temp for temp in range(300,750,50)},
            step=None
        ),
        'u(x=x,y=0) - bottom temperature',
        dcc.Slider( #u(x=x,y=0)
            id='uoy-slider',
            min=300,
            max=700,
            value=500,
            marks={temp: '%s K'%temp for temp in range(300,750,50)},
            step=None
        ), 
        'u(x=x,y=f) - top temperature',
        dcc.Slider( #u(x=x,y=f)
            id='ufy-slider',
            min=300,
            max=700,
            value=500,
            marks={temp: '%s K'%temp for temp in range(300,750,50)},
            step=None
        ),
        'q - heat flux',
        dcc.Slider(
            id='heatflux-slider',
            min=0,
            max=1,
            value=.1,
            marks={flux: '%s mW/m\u00B2'%int(round(flux*1000,0)) for flux in np.linspace(0,1.1,10)},
            step=None
        ), 
        'k - conductivity',
        dcc.Slider(
            id='conductivity-slider',
            min=.00001,
            max=.001,
            value=.0001,
            marks={cond: '%s mW/K'%round(cond*1000,2) for cond in np.linspace(.00001,.001,10)},
            #marks={'label': str(round(cond,5)) for cond in np.linspace(.00001,.001,10)},
            step=None
        )
        ],
        style={'width': '40%', 'padding': '0px 20px 20px 20px', 'display': 'inline-block'}) #end slider div
    ],
    style={'padding': '20px 20px 20px 20px','color': colors['text']}
    ),

])

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
    return {
        'data': [
                    {'z': ugrid, 'type': 'contour', 'name': 'SF','transpose':True,
                    'x':xgrid[:,0],'y':ygrid[0,:]
                    }
        ]
    }
    



if __name__ == '__main__':
    app.run_server(debug=True)