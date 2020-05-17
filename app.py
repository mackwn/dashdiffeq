# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import os


#external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG],suppress_callback_exceptions=True)
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

