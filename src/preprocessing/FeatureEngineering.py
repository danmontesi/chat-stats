import pandas as pd
from CleanDataset import DATASET_PATH
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + "dataset.csv")

    # Change format
    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    df['date'] = [str(x)[:10] for x in df['date_time']]

    # Add 'hour' column
    df['hour'] = df['time'].str[:2]

    # Add first_message column
    df['first_message'] = False

    # Get time difference from previous message
    df['time_difference'] = [x.days * 24 * 60 * 60 + x.seconds for x in (df['date_time'] - df['date_time'].shift(1))]
    df['time_difference'] = df['time_difference'].fillna(-1).astype(int)

    # Flag first message of the day
    first_message_idx = df[df['time'] >= '05:00:00'].sort_values("date_time").drop_duplicates(subset=['date'], keep='first').index
    df.loc[first_message_idx, "first_message"] = True

    # Add 'week of the day' feature
    df['week_day'] = df['date_time'].dt.weekday

    # Add month/year feature
    df['month_year'] = [str(x)[:7] for x in df['date_time']]

    list_ordered_columns = ['date_time', 'date', 'month_year', 'time', 'hour', 'time_difference', 'first_message', 'sender', 'message']
    df = df[list_ordered_columns]
    df.columns = ['date_time', 'date', 'month_year', 'time', 'hour', 'seconds_from_previous_message', 'is_first_message_of_day', 'sender', 'message']

    df.to_csv('../dataset/final_dataset.csv', index=False)