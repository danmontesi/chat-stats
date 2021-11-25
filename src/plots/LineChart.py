from abc import ABC

# import numpy
import numpy as np
# import pandas
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
# import plotly
import plotly.graph_objects as go
import plotly.express as px

import seaborn as sns

from src.preprocessing.CleanDataset import DATASET_PATH

sns.set_style('darkgrid')


class LineChart(ABC):
    def __init__(self, df, value_column, categorical_column, index_column, text_column):
        """
        Given a dataframe, their categorical column, hue column and value column,
        calculates the percentage for each hue value for every category and plots a
        LineChart

        The categories are automatically ordered by the names ascendant

        :param df:
        :param value_column:
        :param categorical_column:
        :param index_column:
        :param text_column:
        """
        self.df = df
        self.value_column = value_column
        self.categorical_column = categorical_column
        self.index_column = index_column
        self.text_column = text_column

    def plot(self):

        list_categories = self.df[self.categorical_column].tolist()

        bar_args = {
            'textposition': "inside",
            'textfont': {'color': 'rgb(255,255,255)'},  # white texts
            'marker_line_color': 'rgb(8,48,107)',
            'marker_line_width': 1
        }

        fig = px.line(self.df, x=self.index_column, y=self.value_column, color=self.categorical_column, text=self.text_column)
        fig.show()

        # Add increment

        # Change the bar mode
        #fig.update_layout(barmode='stack', width=1400, height=800, autosize=True)
        #fig.update_yaxes(title='Monthy Share Messages by Sender')
        #fig.update_xaxes(tickangle=0)



if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + 'final_dataset.csv')

    df = df[df.year_month <= '2018-12']

    # Count for every month, the % times with a message starter / all days with at least a message
    senders_list = df.sender.unique().tolist()

    index_col = 'year_month'
    categorical_col = 'sender'
    value_col = 'is_first_message_of_day'

    df_groupby = df.groupby([index_col, categorical_col]).agg({'is_first_message_of_day': np.sum}).reset_index()
    df_groupby_single_month = df.groupby([index_col]).agg({'is_first_message_of_day': np.sum}).reset_index()

    text_col = 'num_days_with_messages'
    df_groupby_single_month.columns = [index_col, text_col]

    df_plot = pd.merge(df_groupby_single_month, df_groupby, on=index_col, how='inner')
    df_plot[value_col] = np.round(df_plot[value_col] / df_plot['num_days_with_messages'], 1)

    #
    # df_pivot = pd.pivot_table(df, index=index_col, columns=categorical_col, values=value_col, aggfunc=np.sum, fill_value=0)
    #
    # df_pivot[senders_list[1]], df_pivot[senders_list[0]] = df_pivot[senders_list[1]] / (df_pivot[senders_list[0]] + df_pivot[senders_list[1]]), \
    #                                                        df_pivot[senders_list[0]] / (df_pivot[senders_list[0]] + df_pivot[senders_list[1]])
    #
    # # restore as grouped data
    # df_1 = df_pivot[senders_list[0]].reset_index()
    # df_1['sender'] = senders_list[0]
    # df_1.columns = [index_col, value_col, categorical_col]
    #
    # df_2 = df_pivot[senders_list[1]].reset_index()
    # df_2['sender'] = senders_list[1]
    # df_2.columns = [index_col, value_col, categorical_col]

    #df_plot = pd.concat([df_1, df_2])

    lc = LineChart(df_plot, value_col, categorical_col, index_col, text_column = text_col)
    lc.plot()

'''
    df_temp = df.groupby('year_month').agg({'message': len}).reset_index()
    df_temp.columns = ['year_month', 'total_messages']


    df_grouped.columns = ['year_month', 'sender', 'sender_messages']

    df_grouped = pd.merge(df_temp, df_grouped, how='inner', on='year_month')
    df_grouped['sender_percentage_messages'] = round(100 * df_grouped.sender_messages / df_grouped.total_messages, 1)

    df_grouped = df_grouped.sort_values('year_month')

    # Filter by months

    df_grouped = df_grouped[df_grouped.year_month <= '2016-12']

    plot = FullStackedBarchart(df_grouped, 'sender_percentage_messages', 'year_month', 'sender')
    plot.plot()'''
