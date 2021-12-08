# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import  dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import os

from src.plots.EmojiPlots import CountEmojis
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

app.layout = html.Div(id='body',children=[
    html.Div(id='header', children=[
        html.Img(id='logo',
                 src=app.get_asset_url('images/logo.png'),
                 style={'max-width':'15em',
                        'margin-left':'5px',
                        'margin-top': '5px'})
    ], style={'background-color':'white'}),

    html.Div(id='nav-bar',children=[
         dcc.Dropdown(id='chat-dropdown',
                      options=[{'label':x[1:], 'value': x} for i, x in enumerate(chats)],
                      value = chats[0]),
         html.Button('Load Data', id='load-data', n_clicks=0)]
         ),
    html.Div(id='dashboard', children=[
        dcc.Graph()
    ])
    ]
    )







@app.callback(
    Output('dashboard', 'children'),
    Input('load-data', 'n_clicks'),
    State('chat-dropdown', 'value'))
def load_data(n_clicks, value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    print(value)
    main(value, debug=True)
    df = pd.read_csv('./src/dataset/final_dataset.csv')
    print(df.head(20))
    print("HELLOS!")
    fig = CountEmojis(df).fig

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=["type", "scatter"],
                        label="Scatter Plot",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "bar"],
                        label="Bar Chart",
                        method="restyle"
                    )
                ]),
            )]
    )

    return dcc.Graph(figure=fig)

app.run_server(debug=True)