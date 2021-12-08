import pandas as pd
from emoji import UNICODE_EMOJI
import os

DATASET_PATH = os.getcwd() + '/src/dataset/'

def chat_to_df(txt_dir, div_char=']'):

    file_dir = DATASET_PATH + txt_dir
    print(file_dir)

    date = []
    time = []
    sender = []
    message = []

    # Create list of all emojis
    emojis_lst = []
    [emojis_lst.append(x[0]) for x in list(UNICODE_EMOJI['en'])]

    if div_char == ']':

        with open(file_dir) as f:
            for i, line in enumerate(f):


                if line[0] != '[' and not (line[0].isalpha() or line[0] in emojis_lst):
                    continue

                elif line[0] != '[' and (line[0].isalpha() or line[0] in emojis_lst):
                    message[-1] = message[-1] + ' ' + line
                    message[-1] = message[-1].strip('\n')
                    continue

                date.append(line.split(",")[0].strip('[').strip(" "))
                time.append(line.split(div_char)[0].split(",")[1].strip(" "))
                sender.append(line.split(div_char)[1].split(":")[0].strip(" "))
                message.append(line.split(": ")[1].strip('\n').strip(" "))

                if line.split(": ")[1].strip('\n').strip(" ") == "":
                    # print("WARNING: The following line has null message:")
                    # print(f'{i}, {line},\nline[0]: {line[0]}')
                    # print(line.split(": ")[1].strip('\n').strip(" "))
                    message[-1] = " "



        df = pd.DataFrame(
            {'date': date,
             'time': time,
             'sender': sender,
             'message': message
            })


    elif div_char == '-':

        with open(file_dir) as f:
            for i, line in enumerate(f):

                # Remove forwarded messages
                if line[0] == '[':
                    continue

                if len(line) < 6 or (line[2] != '/' or line[5] != '/'):
                    message[-1] = message[-1] + line.strip('\n')
                    continue

                if '‎' in line:
                    continue


                date.append(line.split(",")[0].strip('[').strip(" "))
                time.append(line.split(div_char)[0].split(",")[1].strip(" "))
                sender.append(line.split(div_char)[1].split(":")[0].strip(" "))
                message.append(line.split(": ")[1].strip('\n').strip(" "))

        df = pd.DataFrame(
            {'date': date,
             'time': time,
             'sender': sender,
             'message': message
             })

    df.to_csv(DATASET_PATH + 'dataset.csv', index=False)

    # True = no errors
    return True

