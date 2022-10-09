from Tools.scripts.dutree import display
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk

import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

def percentage(part, whole):
    return 100 * float(part) / float(whole)


def create_wordcloud(text):
    mask = np.array(Image.open("cloud.png"))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",
                   mask=mask,
                   max_words=3000,
                   stopwords=stopwords,
                   repeat=True)
    wc.generate(str(text))
    wc.to_file("wc.png")
    print("Word Cloud Saved Successfully")
    path = "wc.png"
    display(Image.open(path))


tweets = pd.read_csv(open("tweets.csv", "r", encoding="utf8"))
# tweets = tweets[1:10]
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
noOfTweet = len(tweets.count(axis=1))
for tweet in tweets['renderedContent']:
    tweet_list.append(tweet)
#     analysis = TextBlob(tweet)
#     score = SentimentIntensityAnalyzer().polarity_scores(tweet)
#     neg = score['neg']
#     neu = score['neu']
#     pos = score['pos']
#     comp = score['compound']
#     polarity += analysis.sentiment.polarity
#
#     if neg > pos:
#         negative_list.append(tweet)
#         negative += 1
#     elif pos > neg:
#         positive_list.append(tweet)
#         positive += 1
#
#     elif pos == neg:
#         neutral_list.append(tweet)
#         neutral += 1
# positive = percentage(positive, noOfTweet)
# negative = percentage(negative, noOfTweet)
# neutral = percentage(neutral, noOfTweet)
# polarity = percentage(polarity, noOfTweet)
# positive = format(positive, '.1f')
# negative = format(negative, '.1f')
# neutral = format(neutral, '.1f')
#
# tweet_list = pd.DataFrame(tweet_list)
# neutral_list = pd.DataFrame(neutral_list)
# negative_list = pd.DataFrame(negative_list)
# positive_list = pd.DataFrame(positive_list)
# print("total number: ", len(tweet_list))
# print("positive number: ", len(positive_list))
# print("negative number: ", len(negative_list))
# print("neutral number: ", len(neutral_list))

# Cleaning Text (RT, Punctuation etc)
# Creating new dataframe and new features
tw_list = pd.DataFrame(tweet_list)
tw_list["text"] = tw_list[0]
# Removing RT, Punctuation etc
remove_rt = lambda x: re.sub('(RT @\w+: )', " ", x)
rt = lambda x: re.sub("(#[A-Za-z0-9]+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)
tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
tw_list["text"] = tw_list.text.str.lower()
print(tw_list.head())

# Calculating Negative, Positive, Neutral and Compound values
tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tw_list['text'].items():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    if neg > pos:
        tw_list.loc[index, 'sentiment'] = "negative"
    elif pos > neg:
        tw_list.loc[index, 'sentiment'] = "positive"
    else:
        tw_list.loc[index, 'sentiment'] = "neutral"
    tw_list.loc[index, 'neg'] = neg
    tw_list.loc[index, 'neu'] = neu
    tw_list.loc[index, 'pos'] = pos
    tw_list.loc[index, 'compound'] = comp
print(tw_list.head(10))
tw_list_negative = tw_list[tw_list["sentiment"]=="negative"]
tw_list_positive = tw_list[tw_list["sentiment"]=="positive"]
tw_list_neutral = tw_list[tw_list["sentiment"]=="neutral"]
tw_list_positive.to_csv("positive.csv")
tw_list_neutral.to_csv("neutral.csv")
tw_list_negative.to_csv("negative.csv")

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])
#Count_values for sentiment
print(count_values_in_column(tw_list,"sentiment"))
count_values_in_column(tw_list,"sentiment").to_csv("values.csv")
create_wordcloud(tw_list["text"].values)

