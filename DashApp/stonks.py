import datetime
from selenium import webdriver
import time
import webbrowser
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
### Need to import all sklearn._______ modules

#################
# Backend Logic #
#################

# Insert backround data stuff

### In order to make the model easier to load, we should just keep the .pkl file with the ML model saved in the repo, then have the app download the most updated one (will always have the same name).

##################
# Frontend Logic #
##################

app = Dash(__name__)

def serve_layout():

    return html.Div([

        html.Div([
            html.Div(id='live-time'), #'The time is: ' + str(datetime.datetime.now())),
            dcc.Interval(id='live-time-update',interval=3000, n_intervals=0)
        ]),

        html.Div([
            html.H2('The time should be refreshed every three seconds.'),
        ]),

        html.Br(),
        html.Br(),
        html.Br(),

        html.H1('Stock Predictor POC', style={'textAlign': 'center'}),
        
        html.Div([
            html.Div(id='line-graph'),
            dcc.Interval(id='line-graph-update',interval=3000, n_intervals=0)
        ]),

        html.Div([
            html.Div(id = 'next-price'),
            dcc.Interval(id='next-price-update',interval=3000, n_intervals=0)
        ])
    ])

# Create function that re-creates/"re-serves" the app layout

### Allows for the app to `re-serve` itself after the refresh button is hit on the browser (makes it up-to-date)
app.layout = serve_layout

#webbrowser.open("http://localhost:8050/")

#################
# App Callbacks #
#################

#Refreshes the date-time shown on the page every 5 seconds
@app.callback(
    Output('live-time', 'children'),
    Input('live-time-update', 'n_intervals')
)
def time_refresh(n):
    return [
        html.H1('Refresh as of: ' + str(datetime.datetime.now())[:-7])
    ]


@app.callback(
    Output('line-graph', 'children'),
    Input('line-graph-update', 'n_intervals')
)
def graph_refresh(n):
    df = pd.DataFrame({
        'Time': ['09:30', '10:30', '11:30', '12:30', '13:30', '14:30', '15:30', '16:30'],
        'Predicted Close': [round(random.random(), 2) for x in ['09:30', '10:00', '11:00', '12:00', '13:30', '14:30', '15:30', '16:30']],
        'Close': [round(random.random(), 2) for x in ['09:30', '10:00', '11:00', '12:00', '13:30', '14:30', '15:30', '16:30']]
        })



    fig = px.line(df, x="Time", y="Close")

    return [
        dcc.Graph(
            figure=fig
        )
    ]


@app.callback(
    Output('next-price', 'children'),
    Input('next-price-update', 'n_intervals')
)
def nextclose_refresh(n):
    return [
        html.H2(
            children = f'Next Predicted Close Price: ${round(random.random(), 2)}'
        ),
        html.H2(
            children = f'Prediction MSE: ${round(random.random(), 2)/10}'
        )
    ]

if __name__ == '__main__':
    app.run_server(debug=True)