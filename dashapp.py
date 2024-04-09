import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import yfinance as yf
from datetime import datetime

app = dash.Dash(__name__)
server = app.server


nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)

options = [{'label': f'{symbol} {nsdq.loc[symbol]["Name"]}', 'value': symbol} for symbol in nsdq.index]

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight': '30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['TSLA'],
            multi=True
        )
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 24, 'marginLeft': '30px'}
        ),
    ], style={'display': 'inline-block'}),
    dcc.Graph(id='my_graph')
])

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'), State('my_date_picker', 'start_date'), State('my_date_picker', 'end_date')]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []

    for ticker in stock_ticker:
        df = yf.download(ticker, start=start, end=end)
        traces.append({'x': df.index, 'y': df['Close'], 'name': ticker})

    fig = {
        'data': traces,
        'layout': {'title': ', '.join(stock_ticker) + ' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
