import pandas as pd
from emoji import UNICODE_EMOJI


pd.set_option('display.max_columns', 500)
DATASET_PATH = '../dataset/'

def chat_to_df(txt_dir, div_char=']'):
    date = []
    time = []
    sender = []
    message = []

    # Create list of all emojis
    emojis_lst = []
    [emojis_lst.append(x[0]) for x in list(UNICODE_EMOJI['en'])]

    if div_char == ']':

        with open(txt_dir) as f:
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
                    print("WARNING: The following line has null message:")
                    print(f'{i}, {line},\nline[0]: {line[0]}')
                    print(line.split(": ")[1].strip('\n').strip(" "))
                    message[-1] = " "



        df = pd.DataFrame(
            {'date': date,
             'time': time,
             'sender': sender,
             'message': message
            })

        return df

    elif div_char == '-':

        with open(txt_dir) as f:
            for i, line in enumerate(f):

                # Remove forwarded messages
                if line[0] == '[':
                    continue

                if len(line) < 6 or (line[2] != '/' or line[5] != '/'):
                    print(message[-1])
                    message[-1] = message[-1] + line.strip('\n')
                    continue

                if '‎' in line:
                    continue

                print(i)
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



        return df

if __name__ == "__main__":

    file_dir = DATASET_PATH + 'chat_nast_dan.txt'
    df = chat_to_df(file_dir)
    df.to_csv('../dataset/dataset.csv', index=False)
    df_new = pd.read_csv('../dataset/dataset.csv')
