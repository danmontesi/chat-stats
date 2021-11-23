from abc import ABC

# import numpy
import numpy as np
# import pandas
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
# import plotly
import plotly.graph_objects as go
import seaborn as sns

from src.preprocessing.CleanDataset import DATASET_PATH

sns.set_style('darkgrid')

class FullStackedBarchart(ABC):
    def __init__(self, df, value_column, categorical_column, hue_column):
        """
        Given a dataframe, their categorical column, hue column and value column,
        calculates the percentage for each hue value for every category and plots a
        Full Stacked Barchart (vertical).

        The categories are automatically ordered by the names ascendant

        :param df:
        :param value_column:
        :param categorical_column:
        :param hue_column:
        """
        self.df = df
        self.value_column = value_column
        self.categorical_column = categorical_column
        self.hue_column = hue_column


    def plot(self):
        list_hue_names = list(self.df[self.hue_column].unique())

        df_sender_1 = self.df[self.df[self.hue_column]==list_hue_names[0]]
        df_sender_2 = self.df[self.df[self.hue_column]==list_hue_names[1]]

        list_categories = df_sender_1[self.categorical_column].tolist()

        bar_args = {
            'textposition': "inside",
            'textfont': {'color': 'rgb(255,255,255)'},  # white texts
            'marker_line_color': 'rgb(8,48,107)',
            'marker_line_width': 1
        }

        list_bars = []

        values_list = df_sender_1[self.value_column].tolist()
        list_bars.append(
            go.Bar(name=list_hue_names[0], x=df_sender_1[self.categorical_column].tolist(), y=values_list,
                   text=values_list, marker_color='#007681',
                   **bar_args)
        )

        values_list = df_sender_2[self.value_column].tolist()
        list_bars.append(
            go.Bar(name=list_hue_names[1], x=df_sender_2[self.categorical_column].tolist(), y=values_list,
                   text=values_list, marker_color='#0097a7',
                   **bar_args)
        )

        fig = go.Figure(data=list_bars)

        # Add increment

        # Change the bar mode
        fig.update_layout(barmode='stack', width=1400, height=800, autosize=True)
        fig.update_yaxes(title='Monthy Share Messages by Sender')
        fig.update_xaxes(tickangle=0)

        # TODO: sort by ascending

        fig.show()

if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + 'final_dataset.csv')

    df_grouped = df.groupby(['year_month', 'sender']).agg({'message': len}).reset_index()

    df_temp = df.groupby('year_month').agg({'message': len}).reset_index()
    df_temp.columns = ['year_month', 'total_messages']


    df_grouped.columns = ['year_month', 'sender', 'sender_messages']

    df_grouped = pd.merge(df_temp, df_grouped, how='inner', on='year_month')
    df_grouped['sender_percentage_messages'] = round(100 * df_grouped.sender_messages / df_grouped.total_messages, 1)

    df_grouped = df_grouped.sort_values('year_month')

    # Filter by months

    df_grouped = df_grouped[df_grouped.year_month <= '2016-12']

    plot = FullStackedBarchart(df_grouped, 'sender_percentage_messages', 'year_month', 'sender')
    plot.plot()
