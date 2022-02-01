import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import survey, overview, details, home


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/survey':
        return survey.layout
    elif pathname == '/overview':
        return overview.layout
    elif pathname == '/details':
        return details.layout
    else:
        return home.layout
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)