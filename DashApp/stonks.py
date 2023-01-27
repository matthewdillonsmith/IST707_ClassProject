import datetime
from selenium import webdriver
import time
import webbrowser
from dash import Dash, html, dcc, Input, Output
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

# Create function that re-creates/"re-serves" the app layout
def serve_layout():
    return html.Div([
        html.Div(id='live-time-update'), #'The time is: ' + str(datetime.datetime.now())),

        html.Br(),

        html.H2('The time should be refreshed every five seconds.'),

        ### This should allow us to create 'tickers' for the different stocks; as well as for updating time-series graphs.
        dcc.Interval( 
            id='interval-component',
            interval=5000,
            n_intervals=0
        )
    ])


### Allows for the app to `re-serve` itself after the refresh button is hit on the browser (makes it up-to-date)
app.layout = serve_layout

#webbrowser.open("http://localhost:8050/")

#################
# App Callbacks #
#################

#Refreshes the date-time shown on the page every 5 seconds
@app.callback(
    Output('live-time-update', 'children'),
    Input('interval-component', 'n_intervals')
)
def time_refresh(n):
    return [
        html.H1('Refresh as of: ' + str(datetime.datetime.now())[:-7])
    ]

if __name__ == '__main__':
    app.run_server(debug=True)