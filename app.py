# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from elliptic2d import elliptic2dsolve
from dash.dependencies import Input, Output 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[500,500],[1000,500],.1,10,10)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.',
        style={
            'textAlign': 'center',
            'color': colors['text']
    }),

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
    ],style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div(dcc.Slider(
        id='uox-slider',
        min=300,
        max=700,
        value=500,
        marks={str(temp): str(temp) for temp in range(300,750,50)},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})

])

@app.callback(
    Output('elliptic-graph','figure'),
    [Input('uox-slider','value')]
)
def update_figure(selected_temp):
    xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[500,500],[selected_temp,500],.1,10,10)
    return {
        'data': [
                    {'z': ugrid, 'type': 'contour', 'name': 'SF','transpose':True,
                    'x':xgrid[:,0],'y':ygrid[0,:]
                    }
        ]
    }
    



if __name__ == '__main__':
    app.run_server(debug=True)