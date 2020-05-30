print('made it into index')
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

print('import server')
from app import app, server
print('import from module')
from apps import app2del, app1dpar
print('import about')
import about



print('made it into index, server assigned')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

print('assigned layout')
#print('url:')

@app.callback(Output('page-content','children'),
                [Input('url','pathname')])
def display_page(pathname):
    print('pathname:{pathname}'.format(pathname=pathname))
    if pathname == '/app2del': return  app2del.layout
    elif pathname == '/app1dpar': return app1dpar.layout
    elif pathname == '/' : return about.layout
    else: return '404'

if __name__ == '__main__':
    app.run_server(debug=True)