# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import  dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import os

from src.plots.EmojiPlots import EmojisPlot
from src.main import main

app = dash.Dash(__name__)

# Load chats
raw_chats = os.listdir('./src/dataset')

# Remove working files
working_csv = ['final_dataset.csv', 'dataset.csv']

for file in working_csv:
    if file in raw_chats:
        raw_chats.remove(file)

chats = list(map(str.strip, raw_chats))

app.layout = html.Div(id='header',children=[
    html.Div(id='nav-bar', children=[
        html.Img(id='logo',
                 src=app.get_asset_url('images/logo.png'),
                 style={'max-width':'15em',
                        'margin-left':'5px',
                        'margin-top': '5px'})
    ], style={'background-color':'white'}),

    html.Div(id='body',
             children=[
                 dcc.Dropdown(id='chat-dropdown',
                              options=[{'label':x[1:], 'value': x} for i, x in enumerate(chats)],
                              value = chats[0],
                              style = {'width':'20em',
                                       'margin-right':'10px'}),
                 html.Button('Load Data', id='load-data', n_clicks=0)
             ], style={'display':'flex',
                       'justify-content': 'start',
                       'margin':'15px 10px'}),
    html.Div(id='dashboard',

             children=[
                html.Div(id='dashboard-left',
                         children=[
                             dcc.Dropdown(id='frequency-dropdown',
                                          options=[{'label': x, 'value': x} for x in ['day','month', 'all']],
                                          value=chats[0],
                                          style={'width': '20em',
                                                 'margin-right': '10px'}),
                             html.Button('Load Data', id='choose-frequency', n_clicks=0)
                         ],
                         style={'width':'50%',
                                'background-color':'blue'}),
                html.Div(id='dashboard-right',
                         children=[],
                         style={'width':'50%'})
            ], style={'display':'flex'}
    )])

@app.callback(
    Input('load-data', 'n_clicks'),
    State('chat-dropdown', 'value'))
def load_chat(n_clicks, value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return

    main(value, debug=True)


@app.callback(
    Output('dashboard-right', 'children'),
    Input('choose-frequency', 'n_clicks'),
    State('frequency-dropdown', 'value'))
def change_frequency(n_clicks, value):

    df = pd.read_csv('./src/dataset/final_dataset.csv')

    emojis_fig = EmojisPlot(df, value)

    graphs = []
    graphs.append(dcc.Graph(figure=emojis_fig))
    #graphs.append(dcc.Graph(figure=danisss_fig))


    return graphs




app.run_server(debug=False)
