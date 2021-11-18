import pandas as pd
import plotly.graph_objs as go



def message_count(df, by='day'):


    if by == 'day':

        df_messages = df.groupby(by=["date", "sender"]).count()['message'].reset_index()

        fig = go.Figure()

        print(df_messages)
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.message)
            fig.add_bar(x=sender_messages.date, y=sender_messages.message, name=sender)

        fig.show()

    elif by == 'month':

        df_messages = df.groupby(by=["year_month", "sender"]).count()['message'].reset_index()

        fig = go.Figure()

        print(df_messages)
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.message)
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.message, name=sender)

        fig.show()


    elif by == "all":

        df_messages = df.groupby(by=["sender"]).count()['message'].reset_index()

        fig = go.Figure()
        print("all messages")
        print(df_messages)
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.message)
            fig.add_bar(x=sender_messages.sender, y=sender_messages.message, name=sender)

        fig.show()

def word_count(df, by='day'):

    df['words'] = df['message'].str.split(" ").str.len()

    if by == 'day':

        df_words = df.groupby(by=["date", "sender"]).sum()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_words in df_words.groupby('sender'):
            print(sender_words.sender, sender_words.words)
            fig.add_scatter(x=sender_words.date, y=sender_words.words, name=sender, mode='lines')

        fig.show()

    elif by == "month":

        df_messages = df.groupby(by=["year_month", "sender"]).sum()['words'].reset_index()

        fig = go.Figure()

        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.words)
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.words, name=sender)

        fig.show()


    elif by == "all":

        df_messages = df.groupby(by=["sender"]).sum()['words'].reset_index()


        fig = go.Figure()
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.words)
            fig.add_bar(x=sender_messages.sender, y=sender_messages.words, name=sender)

        fig.show()

def avg_words_per_message(df, by='day'):
    df['words'] = df['message'].str.split(" ").str.len()

    if by == 'day':

        df_words = df.groupby(by=["date", "sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        print(df_words)
        for sender, sender_words in df_words.groupby('sender'):
            print(sender_words.sender, sender_words.words)
            fig.add_scatter(x=sender_words.date, y=sender_words.words, name=sender, mode='lines')

        fig.show()

    elif by == "month":

        df_messages = df.groupby(by=["year_month", "sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        print(df_messages)
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.words)
            fig.add_bar(x=sender_messages.year_month, y=sender_messages.words, name=sender)

        fig.show()

    elif by == "all":

        df_messages = df.groupby(by=["sender"]).mean()['words'].reset_index()

        fig = go.Figure()

        print(df_messages)
        for sender, sender_messages in df_messages.groupby('sender'):
            print(sender_messages.sender, sender_messages.words)
            fig.add_bar(x=sender_messages.sender, y=sender_messages.words, name=sender)

        fig.show()


if __name__ == "__main__":
    df = pd.read_csv("../dataset/final_dataset.csv")

    message_count(df, 'month')
    word_count(df, 'month')
    avg_words_per_message(df, 'month')
