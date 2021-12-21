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

from src.plots.EmojiPlots import CountEmojis
from src.main import main


class App():

    def main(self):
    app = dash.Dash(__name__)

    # Load chats
    raw_chats = os.listdir('./src/dataset')

    # Remove working files
    working_csv = ['final_dataset.csv', 'dataset.csv']

    for file in working_csv:
        if file in raw_chats:
            raw_chats.remove(file)

    chats = list(map(str.strip, raw_chats))

    app.layout = html.Div(id='body',children=[
        html.Div(id='header', children=[
            html.Img(id='logo',
                     src=app.get_asset_url('images/logo.png'),
                     style={'max-width':'15em',
                            'margin-left':'5px',
                            'margin-top': '5px'})
        ], style={'background-color':'white'}),

        html.Div(id='nav-bar',
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
                                              options=[{'label': x[1:], 'value': x} for x in ['day','month', 'all']],
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
        Output('dashboard-left', 'children'),
        Input('load-data', 'n_clicks'),
        State('chat-dropdown', 'value'))
    def load_data(n_clicks, value):
        ctx = dash.callback_context


        graphs = []

        if not ctx.triggered:
            return

        main(value, debug=True)
        df = pd.read_csv('./src/dataset/final_dataset.csv')



    @app.callback(
        Output('dashboard-left', 'children'),
        Input('choose-frequency', 'n_clicks'),
        State('frequency-dropdown', 'value'))
    def load_data(n_clicks, value):
        emojis_fig = go.Figure()

        graphs = []

        if value == 'month':
            for sender, sender_emojis in self.df.groupby('sender'):
                emojis_fig.add_scatter(x=sender_emojis.year_month, y=sender_emojis.emojis_count, name = sender)

        elif value == 'day':
            for sender, sender_emojis in self.df.groupby('sender'):
                emojis_fig.add_scatter(x=sender_emojis.date, y=sender_emojis.emojis_count, name = sender)

        elif value == 'all':
            for sender, sender_emojis in emojis_fig.df.groupby('sender'):
                emojis_fig.add_bar(x=sender_emojis.sender, y=sender_emojis.emojis_count, name = sender)


        graphs.append(dcc.Graph(figure=emojis_fig))

        return graphs

