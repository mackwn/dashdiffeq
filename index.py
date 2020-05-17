import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

from app import app
#from app import server
from apps import app2del, app1dpar
import about

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content','children'),
                [Input('url','pathname')])
def display_page(pathname):
    if pathname == '/app2del': return  app2del.layout
    elif pathname == '/app1dpar': return app1dpar.layout
    elif pathname == '/' : return about.layout
    else: return '404'

if __name__ == '__main__':
    app.run_server(debug=True)