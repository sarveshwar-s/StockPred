from textblob import TextBlob
import tweepy as tw
import requests as req
import os
import pandas as pd

consumer_key= 'YOUR_CONSUMER_KEY'
consumer_secret= 'YOUR_CONSUMER_SECRET_KEY'
access_token= 'YOUR_ACCESS_TOKEN'
access_token_secret= 'YOUR_SECRET_ACCESS_TOKEN'

def twitter_analysis(compname):
    auth = tw.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    search_words = compname
    search_words = search_words + " " + "-filter:retweets"
    date_since = "2020-03-05"

    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(10)
    total = 0
    positive = 0
    negative = 0
    neutral = 0
    for items in tweets:
        print("====================================================================")
        print(items.text)
        blobs = TextBlob(items.text)
        for sentence in blobs.sentences:
            print(sentence.sentiment.polarity)
            if(sentence.sentiment.polarity > 0 ):
                positive+=1
            elif(sentence.sentiment.polarity < 0):
                negative+=1
            else:
                neutral+=1
            total+=sentence.sentiment.polarity
    positive_perentage = (positive/10)*100
    negative_percentage = (negative/10)*100
    neutral_percentage = 100-(positive_perentage + negative_percentage)
    print("positive  %", positive_perentage, "negative %", negative_percentage, "neutral %", neutral_percentage)
    print(total)
    persentlist = []
    persentlist.append(positive_perentage)
    persentlist.append(negative_percentage)
    persentlist.append(neutral_percentage)
    return persentlist

# vals = twitter_analysis("amazon")
# for i in vals:
#     print(i)
