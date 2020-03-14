from textblob import TextBlob
# from textblob.sentiments import NaiveBayesAnalyzer
import requests as req

# api = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=GOOG&api-key=rN5bN0aS0mOuHgcx2MnaA2Ilu2lTMUHJ"


# print(datas["response"]["docs"][0]["lead_paragraph"]) #This is for newyork times
def news_analysis(compname):
    positive = 0
    negative = 0
    neutral = 0
    api = "http://newsapi.org/v2/everything?q="+ compname +"&apiKey=5c91d5fe23a441aa8301bd5c08759185"
    responses = req.get(api)
    datas = responses.json()
    articles_len = len(datas["articles"])
    for items in range(0,articles_len):
        sentences = datas["articles"][items]["description"]
        blobs = TextBlob(sentences)
        print(blobs.sentences)
        for sentence in blobs.sentences:
            print(sentence.sentiment.polarity)
            if(sentence.sentiment.polarity > 0 ):
                positive+=1
            elif(sentence.sentiment.polarity < 0):
                negative+=1
            else:
                neutral+=1
            # sentence.accracy
    positive_perentage = (positive/100)*100
    negative_percentage = (negative/100)*100
    neutral_percentage = 100-(positive_perentage + negative_percentage)
    persentlist = []
    persentlist.append(positive_perentage)
    persentlist.append(negative_percentage)
    persentlist.append(neutral_percentage)
    return persentlist