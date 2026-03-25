import os
from textblob import TextBlob
import requests
import logging

logger = logging.getLogger(__name__)

def news_analysis(compname):
    """Analyze news sentiment for a company"""
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        logger.warning("NEWS_API_KEY not found, returning neutral sentiment")
        return [33.33, 33.33, 33.34]  # Default neutral sentiment
    
    positive = 0
    negative = 0
    neutral = 0
    
    try:
        api_url = "http://newsapi.org/v2/everything"
        params = {'q': compname, 'apiKey': api_key, 'pageSize': 20}
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'articles' not in data:
            logger.warning("No articles found in API response")
            return [33.33, 33.33, 33.34]
        
        articles = data['articles']
        total_sentences = 0
        
        for article in articles:
            description = article.get('description')
            if description:
                blob = TextBlob(description)
                for sentence in blob.sentences:
                    sentiment = sentence.sentiment.polarity
                    total_sentences += 1
                    
                    if sentiment > 0.1:
                        positive += 1
                    elif sentiment < -0.1:
                        negative += 1
                    else:
                        neutral += 1
        
        if total_sentences == 0:
            return [33.33, 33.33, 33.34]
            
        positive_percentage = (positive / total_sentences) * 100
        negative_percentage = (negative / total_sentences) * 100 
        neutral_percentage = (neutral / total_sentences) * 100
        
        return [positive_percentage, negative_percentage, neutral_percentage]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news data: {e}")
        return [33.33, 33.33, 33.34]  # Return neutral sentiment on error
    except Exception as e:
        logger.error(f"Error analyzing news sentiment: {e}")
        return [33.33, 33.33, 33.34]
