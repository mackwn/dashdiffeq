# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc

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

def render_slider(label,vmin,vmax,symbol,units): ###rewrite this to only do the slider formating, and then use list comprehension instead of for loop

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



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col( #Graph 
            'graph',
            md=6,sm=12
        ),
        dbc.Col([
            render_slider(label=key,vmin=value[0],vmax=value[1],
                symbol=value[2],units=value[3]) for key, value in slider_labels.items() # rainbows
        ],
            md=6,sm=12
        )
    ])
])



# app.layout = html.Div(children=[
#     html.H1(
#         children='Interactive 2D Heat Equation',
#         style={
#             #'textAlign': 'center',
#             #'color': colors['text']
#         }
#     ),




#     dcc.Tabs([
#         dcc.Tab(label='Steady-State 2D', children=[

#         html.Div(children='q = -k\u2207\u00B2',
#             style={
#                 'textAlign': 'center'#,
#                 #'color': colors['text']
#         }),


#         html.Div([
        
#         ##Div for graph
#             html.Div([
#                 dcc.Graph(
#                     id='elliptic-graph',
#                     figure={
#                         'data': [
#                             {'z': ugrid, 'type': 'contour', 'name': 'SF','transpose':True,
#                             'x':xgrid[:,0],'y':ygrid[0,:]
#                             },
#                         ],
#                         'layout': {
#                             'plot_bgcolor': colors['background'],
#                             'paper_bgcolor': colors['background'],
#                             'font': {
#                                 'color': colors['text']
#                             }
#                         }
#                     }
#                 )
#             ],style={'width': '40%', 'display': 'inline-block', 'padding': '0 20'}),

        
#             #Div for sliders
#             html.Div([

#             html.Div(['u(x=0,y=y): ',html.Span(id='uox-slider-output-container'),' K']),    

#             dcc.Slider( #u(x=0,y=y)
#                 id='uox-slider',
#                 min=200,
#                 max=800,
#                 value=500,
#                 step=25
#                 #marks={temp: '%s K'%temp for temp in range(300,750,50)},
#                 #step=None
#             ),
#             html.Div(['u(x=f,y=y): ',html.Span(id='ufx-slider-output-container'),' K']),
#             dcc.Slider( #u(x=f,y=y)
#                 id='ufx-slider',
#                 min=200,
#                 max=800,
#                 value=500,
#                 step=25,

#                 #marks={temp: '%s K'%temp for temp in range(300,750,50)},
#                 #step=None
#             ),
#             html.Div(['u(x=x,y=0): ',html.Span(id='uoy-slider-output-container'),' K']),
#             dcc.Slider( #u(x=x,y=0)
#                 id='uoy-slider',
#                 min=200,
#                 max=800,
#                 value=500,
#                 step=25
#                 #marks={temp: '%s K'%temp for temp in range(300,750,50)},
#                 #step=None
#             ), 
#             html.Div(['u(x=x,y=f): ',html.Span(id='ufy-slider-output-container'),' K']),
#             dcc.Slider( #u(x=x,y=f)
#                 id='ufy-slider',
#                 min=200,
#                 max=800,
#                 value=500,
#                 step=25
#                 #marks={temp: '%s K'%temp for temp in range(300,750,50)},
#                 #step=None
#             ),
#             html.Div(['q: ',html.Span(id='heatflux-slider-output-container'),' mW/m\u00B2']),
#             dcc.Slider(
#                 id='heatflux-slider',
#                 min=0,
#                 max=1,
#                 step=.05,
#                 value=.5
#                 #marks={flux: '%s mW/m\u00B2'%int(round(flux*1000,0)) for flux in np.linspace(0,1.1,10)},
#                 #step=None
#             ), 
#             html.Div(['k: ',html.Span(id='conductivity-slider-output-container'),' mW/K']),
#             dcc.Slider(
#                 id='conductivity-slider',
#                 min=.00001,
#                 max=.00101,
#                 value=.00051,
#                 step=.00005
#                 #marks={cond: '%s mW/K'%round(cond*1000,2) for cond in np.linspace(.00001,.001,10)},
#                 #marks={'label': str(round(cond,5)) for cond in np.linspace(.00001,.001,10)},
#                 #step=None
#             )
#             ],
#             style={'width': '40%', 'padding': '20px 20px 20px 20px', 'display': 'inline-block'}) #end slider div
#         ],
#         style={'padding': '20px 20px 20px 20px','color': colors['text']}
#         )
#         ]),
#         dcc.Tab(label='Transient 1D', children=[

#             html.Div(children='dq/dt = -k\u2207\u00B2',
#                 style={
#                     'textAlign': 'center'#,
#                    # 'color': colors['text']
#             })
#         ])
#     ])  

# ])


for slider in ['uox-slider','ufx-slider','uoy-slider','ufy-slider','heatflux-slider','conductivity-slider']:
    @app.callback(
        Output('%s-output-container'%slider, 'children'),
        [Input(slider, 'value')])
    def update_output(value):
        return value

# @app.callback(
#     Output('elliptic-graph','figure'),
#     [Input('uox-slider','value'),
#     Input('ufx-slider','value'),
#     Input('uoy-slider','value'),
#     Input('ufy-slider','value'),
#     Input('heatflux-slider','value'),
#     Input('conductivity-slider','value'),
    
#     ]
# )
# def update_figure(uox,ufx,uoy,ufy,flux,conduc):
#     xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[uoy,ufy],[uox,ufx],flux,conduc,10,10)
#     return {
#         'data': [
#                     {'z': ugrid, 'type': 'contour', 'name': 'SF','transpose':True,
#                     'x':xgrid[:,0],'y':ygrid[0,:]
#                     }
#         ]
#     }
    



if __name__ == '__main__':
    app.run_server(debug=True)