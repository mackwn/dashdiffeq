import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server
from apps import app2del, app1dpar
import about


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
    if pathname == '/apps/app2del': return  app2del.layout
    elif pathname == '/apps/app1dpar': return app1dpar.layout
    elif pathname == '/about' : return about.layout
    else: return '404'

if __name__ == '__main__':
    app.run_server(debug=True)