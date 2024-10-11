import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout with boxes for each metric
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Time since last successful update of data"),
            dbc.CardBody(html.H4(id='update-time', className='card-title'))
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Time since last scan"),
            dbc.CardBody(html.H4(id='last-scan', className='card-title'))
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Number of scans run this week"),
            dbc.CardBody(html.H4(id='scans-this-week', className='card-title'))
        ]), width=4),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Number of new vulnerabilities found this week"),
            dbc.CardBody(html.H4(id='new-vulnerabilities', className='card-title'))
        ]), width=6),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Number of vulnerabilities remediated this week"),
            dbc.CardBody(html.H4(id='remediated-vulnerabilities', className='card-title'))
        ]), width=6),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=15*60*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('update-time', 'children'),
    Output('last-scan', 'children'),
    Output('scans-this-week', 'children'),
    Output('new-vulnerabilities', 'children'),
    Output('remediated-vulnerabilities', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    # Replace with your API endpoint and logic to extract relevant data
    response = requests.get('https://api.example.com/data')
    data = response.json()

    # Here, you'd extract and compute the metrics
    last_update_time = data['last_update_time']  # Assume this is in a suitable format
    last_scan_time = data['last_scan_time']      # Same as above
    scans_this_week = data['scans_this_week']
    new_vulnerabilities = data['new_vulnerabilities']
    remediated_vulnerabilities = data['remediated_vulnerabilities']

    # Calculate time since last successful update
    time_since_update = datetime.now() - datetime.fromisoformat(last_update_time)
    time_since_scan = datetime.now() - datetime.fromisoformat(last_scan_time)

    return (
        str(time_since_update),  # E.g., "1 hour 30 minutes"
        str(time_since_scan),
        scans_this_week,
        new_vulnerabilities,
        remediated_vulnerabilities
    )

if __name__ == '__main__':
    app.run_server(debug=True)
