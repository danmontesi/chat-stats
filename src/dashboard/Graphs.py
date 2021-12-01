import pandas as pd
import plotly.graph_objs as go

def message_count(df, by='day'):


    if by == 'day':

        df_messages = df.groupby(by=["date", "sender"]).count()['message'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.date, y=sender_messages.message, name=sender)

        return fig

    elif by == 'month':

        df_messages = df.groupby(by=["year_month", "sender"]).count()['message'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.message, name=sender)

        return fig


    elif by == "all":

        df_messages = df.groupby(by=["sender"]).count()['message'].reset_index()

        fig = go.Figure()
        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.sender, y=sender_messages.message, name=sender)

        return fig

def word_count(df, by='day'):

    df['words'] = df['message'].str.split(" ").str.len()

    if by == 'day':

        df_words = df.groupby(by=["date", "sender"]).sum()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_words in df_words.groupby('sender'):
            fig.add_scatter(x=sender_words.date, y=sender_words.words, name=sender, mode='lines')

        return fig

    elif by == "month":

        df_messages = df.groupby(by=["year_month", "sender"]).sum()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.words, name=sender)

        return fig


    elif by == "all":

        df_messages = df.groupby(by=["sender"]).sum()['words'].reset_index()


        fig = go.Figure()
        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.sender, y=sender_messages.words, name=sender)

        return fig

def avg_words_per_message(df, by='day'):
    df['words'] = df['message'].str.split(" ").str.len()

    if by == 'day':

        df_words = df.groupby(by=["date", "sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_words in df_words.groupby('sender'):
            fig.add_scatter(x=sender_words.date, y=sender_words.words, name=sender, mode='lines')

        return fig

    elif by == "month":

        df_messages = df.groupby(by=["year_month", "sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.words, name=sender)

        return fig

    elif by == "all":

        df_messages = df.groupby(by=["sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            fig.add_bar(x=sender_messages.sender, y=sender_messages.words, name=sender)

        return fig


if __name__ == "__main__":
    df = pd.read_csv("../dataset/final_dataset.csv")

    # Filter dates
    df = df[(df.date <= '2017-12-31')&(df.date >= '2017-01-01')]

    message_count(df, 'month')
    word_count(df, 'all').show()
    avg_words_per_message(df, 'month')

