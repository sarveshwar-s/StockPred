import os
from textblob import TextBlob
import tweepy
import logging

logger = logging.getLogger(__name__)


def twitter_analysis(compname):
    """Analyze Twitter sentiment for a company"""
    # Get Twitter API credentials from environment
    consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
    consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    # Check if all credentials are available
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        logger.warning("Twitter API credentials not found, returning neutral sentiment")
        return [33.33, 33.33, 33.34]  # Default neutral sentiment
    
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        search_words = f"{compname} -filter:retweets"
        
        tweets = tweepy.Cursor(
            api.search_tweets, 
            q=search_words, 
            lang="en", 
            tweet_mode='extended'
        ).items(20)  # Increase sample size
        
        positive = 0
        negative = 0
        neutral = 0
        total_tweets = 0
        
        for tweet in tweets:
            blob = TextBlob(tweet.full_text)
            sentiment = blob.sentiment.polarity
            total_tweets += 1
            
            if sentiment > 0.1:
                positive += 1
            elif sentiment < -0.1:
                negative += 1
            else:
                neutral += 1
        
        if total_tweets == 0:
            return [33.33, 33.33, 33.34]
            
        positive_percentage = (positive / total_tweets) * 100
        negative_percentage = (negative / total_tweets) * 100
        neutral_percentage = (neutral / total_tweets) * 100
        
        return [positive_percentage, negative_percentage, neutral_percentage]
        
    except tweepy.TooManyRequests:
        logger.warning("Twitter API rate limit exceeded")
        return [33.33, 33.33, 33.34]
    except Exception as e:
        logger.error(f"Error analyzing Twitter sentiment: {e}")
        return [33.33, 33.33, 33.34]
# for i in vals:
#     print(i)
