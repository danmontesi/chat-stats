import pandas as pd
from CleanDataset import DATASET_PATH
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + "dataset.csv")

    # Change format
    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%y")

    # Add 'hour' column
    df['hour'] = df['time'].str[:2]

    # Add first_message column
    df['first_message'] = False
    df['time_difference'] = -42.4

    # Get time difference from previous message
    df['time_difference'] = [(x.days * 24 * 60 * 60) + x.seconds for x in (df['date_time'] - df['date_time'].shift(-1))]

    # Flag first message of the day
    days_with_messages = df['date'].unique()

    first_message_idx = df[df['time'] >= '05:00:00'].sort_values("date_time").drop_duplicates(subset=['date'], keep='first').index
    df.loc[first_message_idx, "first_message"] = True

    df['week_day'] = df['date'].dt.weekday
    print(df)

    df.to_csv('../dataset/tmp.csv', index=False)




