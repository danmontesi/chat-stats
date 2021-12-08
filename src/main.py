from src.preprocessing.CleanDataset import chat_to_df
from src.preprocessing.FeatureEngineering import preprocess_chat




def main(chat, debug=False):
    if chat[0] == ']' or chat[0] == '-':
        chat_to_df(chat, div_char=chat[0])
    else:
        chat_to_df(chat)

    preprocess_chat(debug=debug)