import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from abc import ABC

# import numpy
import numpy as np
# import pandas
import pandas as pd

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
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

    def get_wordcloud(self, text: str):
        wc = WordCloud(width=800, height=800,
                  background_color='white',
                  min_font_size=10).generate(text)
        return wc

    def clean_text(self, sender):

        text = ' '.join(self.df[self.df[self.sender_column] == sender][self.text_column].astype('str').tolist())

        # clean text removing words having length <= l (l=2 would be enough)
        def remove_short_words(list_words, l=2):
            list_words = [x for x in list_words if len(x) > l]
            return list_words

        text = text.lower()

        list_words = text.split(' ')
        list_words = remove_short_words(list_words)

        to_remove_words = list(set(stopwords.words('italian'))) + ['comunque', 'ora']
        # remove stopwords in italian
        list_words = [word for word in list_words if word not in to_remove_words and ('hah' not in word)]

        return ' '.join(list_words)

    def plot_2_wordcloud(self):
        # extract text for the 2 senders
        list_senders = self.df[self.sender_column].unique().tolist()

        text_sender_1 = self.clean_text(list_senders[0])
        text_sender_2 = self.clean_text(list_senders[1])

        # get wordclouds
        wc_1 = self.get_wordcloud(text_sender_1)
        wc_2 = self.get_wordcloud(text_sender_2)

        list_wc = [wc_1, wc_2]

        plt.figure(figsize=(10, 10))

        for i in range(len(list_wc)):
            plt.subplot(2, 1, i+1).set_title("Sender: " + list_senders[i])
            plt.plot()

            plt.imshow(list_wc[i])
            plt.axis('off')

        plt.suptitle('WordCloud Chat from {} to {}'.format(self.start_date, self.end_date))
        plt.show()

    def plot_single_wordcloud(self):
        # extract text for the 2 senders
        list_senders = self.df[self.sender_column].unique().tolist()

        text_sender_1 = self.clean_text(list_senders[0])
        text_sender_2 = self.clean_text(list_senders[1])

        wordcloud = self.get_wordcloud(text_sender_1 + text_sender_2)
        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.title('WordCloud Chat from {} to {}'.format(self.start_date, self.end_date))
        plt.show()


if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH + 'final_dataset.csv')
    nltk.download('stopwords')
    print(stopwords.words('italian'))
    wc = WordCloudChat(df, '2017-10-01', '2019-01-01', 'message', 'sender')

    wc.plot_2_wordcloud()
