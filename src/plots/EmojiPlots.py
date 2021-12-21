import pandas as pd
import plotly.graph_objs as go
from emoji import UNICODE_EMOJI

pd.set_option('display.max_columns', 500)
class CountEmojis():
    def __init__(self, df, emojis='love'):


        # emojis_lst = []
        # [emojis_lst.append(x[0]) for x in list(UNICODE_EMOJI['en'])]
        if emojis == 'love':
            emojis_lst = ['❤', '🥰', '😍', '😘', '💕', '💙', '💜', '❣', '💚', '💞', '💖', '💛', \
                           '🖤', '💗', '💌', '💓', '😻', '🧡', '💘', '💝', '😽', '‍💟', '‍❤', '️💏', \
                           '🏩', '💒', '🤎', '🤍', '‍💒']

        self.df = df
        self.df['emojis_count'] = 0
        multi_index = [df['date'], df['sender']]

        for emoji in emojis_lst:
            # Emoji count per message
            self.df['emojis_count'] = self.df['emojis_count'] + self.df.message.str.count(emoji)

        # Emoji count per month
        monthly_df = self.df.groupby(by=["year_month", "sender"])['emojis_count'].sum().reset_index()
        self.df = pd.merge(df,
                      monthly_df,
                      how='left',
                      left_on=['year_month', 'sender'],
                      right_on=['year_month','sender'],
                      suffixes=[None, '_monthly'])

        # Emoji count per day
        daily_df= self.df.groupby(by=["date", "sender"]).count()['emojis_count'].reset_index()
        self.df = pd.merge(df,
                      daily_df,
                      how='left',
                      left_on=['date', 'sender'],
                      right_on=['date','sender'],
                      suffixes=[None, '_daily'])

        # Emoji count for the whole period
        all_emojis = self.df.groupby(by=["sender"]).count()['emojis_count'].reset_index()
        self.df = pd.merge(df,
                      all_emojis,
                      how='left',
                      left_on=['sender'],
                      right_on=['sender'],
                      suffixes=[None, '_all'])




if __name__ == '__main__':
    df = pd.read_csv('../dataset/final_dataset.csv')

    fig = CountEmojis(df)