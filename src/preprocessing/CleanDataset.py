import pandas as pd

pd.set_option('display.max_columns', 500)
DATASET_PATH = '../dataset/'

def chat_to_df(txt_dir, div_char=']'):
    date = []
    time = []
    sender = []
    message = []

    with open(txt_dir) as f:
        for line in f:
            if line[0] != '[':
                continue
            date.append(line.split(",")[0].strip('[').strip(" "))
            time.append(line.split(div_char)[0].split(",")[1].strip(" "))
            sender.append(line.split(div_char)[1].split(":")[0].strip(" "))
            message.append(line.split(":")[-1].strip('\n').strip(" "))

    df = pd.DataFrame(
        {'date': date,
         'time': time,
         'sender': sender,
         'message': message
        })

    return df

if __name__ == "__main__":

    file_dir = DATASET_PATH + 'chat_nico_dan.txt'
    df = chat_to_df(file_dir)
    df.to_csv('../dataset/dataset.csv', index=False)
    df_new = pd.read_csv('../dataset/dataset.csv')