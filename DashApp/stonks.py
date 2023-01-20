import datetime
from dash import Dash, html, dcc

app = Dash(__name__)

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))

app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)