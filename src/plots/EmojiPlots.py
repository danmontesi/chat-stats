import pandas as pd
import plotly.graph_objs as go
from emoji import UNICODE_EMOJI

pd.set_option('display.max_columns', 500)
def EmojisPlot(df_data, value, emojis='love'):

    # emojis_lst = []
    # [emojis_lst.append(x[0]) for x in list(UNICODE_EMOJI['en'])]
    if emojis == 'love':
        emojis_lst = ['❤', '🥰', '😍', '😘', '💕', '💙', '💜', '❣', '💚', '💞', '💖', '💛', \
                       '🖤', '💗', '💌', '💓', '😻', '🧡', '💘', '💝', '😽', '‍💟', '‍❤', '️💏', \
                       '🏩', '💒', '🤎', '🤍', '‍💒']

    df = df_data
    df['emojis_count'] = 0
    multi_index = [df['date'], df['sender']]

    for emoji in emojis_lst:
        # Emoji count per message
        df['emojis_count'] = df['emojis_count'] + df.message.str.count(emoji)

    # Emoji count per month
    monthly_df = df.groupby(by=["year_month", "sender"])['emojis_count'].sum().reset_index()
    df = pd.merge(df_data,
                  monthly_df,
                  how='left',
                  left_on=['year_month', 'sender'],
                  right_on=['year_month','sender'],
                  suffixes=[None, '_monthly'])

    # Emoji count per day
    daily_df= df.groupby(by=["date", "sender"]).count()['emojis_count'].reset_index()
    df = pd.merge(df_data,
                  daily_df,
                  how='left',
                  left_on=['date', 'sender'],
                  right_on=['date','sender'],
                  suffixes=[None, '_daily'])

    # Emoji count for the whole period
    all_emojis = df.groupby(by=["sender"]).count()['emojis_count'].reset_index()
    df = pd.merge(df_data,
                  all_emojis,
                  how='left',
                  left_on=['sender'],
                  right_on=['sender'],
                  suffixes=[None, '_all'])

    emojis_fig = go.Figure()

    if value == 'month':
        for sender, sender_emojis in df.groupby('sender'):
            emojis_fig.add_scatter(x=sender_emojis.year_month, y=sender_emojis.emojis_count, name=sender)

    elif value == 'day':
        for sender, sender_emojis in df.groupby('sender'):
            emojis_fig.add_scatter(x=sender_emojis.date, y=sender_emojis.emojis_count, name=sender)

    elif value == 'all':
        for sender, sender_emojis in df.groupby('sender'):
            emojis_fig.add_bar(x=sender_emojis.sender, y=sender_emojis.emojis_count, name=sender)

    return emojis_fig

if __name__ == '__main__':
    df = pd.read_csv('../dataset/final_dataset.csv')

    fig = CountEmojis(df)