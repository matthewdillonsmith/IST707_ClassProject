from dash import Dash, dcc, html, Input, Output
import pandas_datareader.data as web
from sklearn.linear_model import LinearRegression
import numpy as np

app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Stock Predictions'),

    html.Div(children='''
        Enter a stock symbol to predict future prices:
    '''),

    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    stock_symbol = input_data
    df = web.DataReader(stock_symbol, data_source='yahoo', start='01/01/2010')

    # Create a Linear Regression model and fit it to the data
    model = LinearRegression()
    model.fit(np.arange(len(df)).reshape(-1,1), df['Close'])

    # Make predictions for the next 30 days
    future_predictions = model.predict(np.arange(len(df)+30).reshape(-1,1))

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df['Close'], 'type': 'line', 'name': stock_symbol},
                {'x': np.arange(len(df)+30), 'y': future_predictions, 'type': 'line', 'name': 'Prediction'},
            ],
            'layout': {
                'title': stock_symbol + ' Stock Price Predictions'
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
