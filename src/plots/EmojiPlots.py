import pandas as pd
import plotly.graph_objs as go
from emoji import UNICODE_EMOJI


class CountEmojis():
    def __init__(self, df, emojis='love', by='month'):


        # emojis_lst = []
        # [emojis_lst.append(x[0]) for x in list(UNICODE_EMOJI['en'])]
        if emojis == 'love':
            emojis_lst = ['❤', '🥰', '😍', '😘', '💕', '💙', '💜', '❣', '💚', '💞', '💖', '💛', \
                           '🖤', '💗', '💌', '💓', '😻', '🧡', '💘', '💝', '😽', '‍💟', '‍❤', '️💏', \
                           '🏩', '💒', '🤎', '🤍', '‍💒']

        self.df = df
        self.by = by
        self.df['emojis_count'] = 0

        for emoji in emojis_lst:
            self.df['emojis_count'] = self.df['emojis_count'] + self.df.message.str.count(emoji)

        if self.by == 'month':
            self.df = self.df.groupby(by=["year_month", "sender"]).count()['emojis_count'].reset_index()
            self.group_by = "year_month"

        elif self.by == 'day':
            self.df = self.df.groupby(by=["date", "sender"]).count()['emojis_count'].reset_index()
            self.group_by = "day"

        elif self.by == 'all':
            self.df = self.df.groupby(by=["sender"]).count()['emojis_count'].reset_index()


        self.fig = go.Figure()

        if self.by == 'month':
            for sender, sender_emojis in self.df.groupby('sender'):
                self.fig.add_scatter(x=sender_emojis.year_month, y=sender_emojis.emojis_count, name=sender)

        elif self.by == 'day':
            for sender, sender_emojis in self.df.groupby('sender'):
                self.fig.add_scatter(x=sender_emojis.date, y=sender_emojis.emojis_count, name=sender)

        elif self.by == 'all':
            for sender, sender_emojis in self.df.groupby('sender'):
                self.fig.add_bar(x=sender_emojis.sender, y=sender_emojis.emojis_count, name=sender)



if __name__ == '__main__':
    df = pd.read_csv('../dataset/final_dataset.csv')

    fig = CountEmojis(df, love_emojis, by='month')
    fig.fig.show()
    fig = CountEmojis(df, love_emojis, by='day')
    fig.fig.show()
    fig = CountEmojis(df, emojis='love', by='month')
    fig.fig.show()