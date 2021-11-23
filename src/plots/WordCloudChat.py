import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from abc import ABC

# import numpy
import numpy as np
# import pandas
import pandas as pd

import matplotlib.pyplot as plt
from nltk.corpus import stopwords

nltk.download('stopwords')

from src.preprocessing.CleanDataset import DATASET_PATH


class WordCloudChat(ABC):
    def __init__(self, df, start_date, end_date, text_column, sender_column):
        """
        Given a dataframe of messages between 2 people, extracts a wordcloud out of it with
        the most frequent words. (observation: visualization settings need to be modified by the class)

        :param df:
        :param start_date:
        :param end_date:
        :param text_column:
        :param sender_column:
        """

        self.df = df
        self.start_date = start_date
        self.end_date = end_date
        self.text_column = text_column
        self.sender_column = sender_column

        # filter dataset

        self.df = self.df[(self.df.date >= start_date) & (self.df.date <= end_date)]

    def clean_text(self, text: str):
        # clean text removing words having length <= l (l=2 would be enough)
        def remove_short_words(list_words, l=2):
            list_words = [x for x in list_words if len(x) > l]
            return list_words

        text = text.lower()

        list_words = text.split(' ')
        list_words = remove_short_words(list_words)

        # remove stopwords in italian
        list_words = [word for word in list_words if word not in list(set(stopwords.words('italian')))]

        return ' '.join(list_words)

    def plot(self):
        # extract text for the 2 senders

        list_senders = self.df[self.sender_column].unique().tolist()

        text_sender_1 = ' '.join(self.df[self.df[self.sender_column] == list_senders[0]][self.text_column].astype('str').tolist())

        text_sender_2 = ' '.join(self.df[self.df[self.sender_column] == list_senders[1]][self.text_column].astype('str').tolist())

        text_sender_1 = self.clean_text(text_sender_1)
        text_sender_2 = self.clean_text(text_sender_2)
        # visualize wordcloud
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=stopwords,
                              min_font_size=10).generate(text_sender_1 + text_sender_2)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()


if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + 'final_dataset.csv')

    wc = WordCloudChat(df, '2015-01-01', '2016-01-01', 'message', 'sender')
    wc.plot()
