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

        The categories are automatically ordered by the names ascendant, and they are assumed t obe always 2 (2 senders)

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
        fig = px.line(self.df, x=self.index_column, y=self.value_column, color=self.categorical_column, **bar_args)
        fig.show()



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

    lc = LineChart(df_plot, value_col, categorical_col, index_col, text_column = text_col)
    lc.plot()
