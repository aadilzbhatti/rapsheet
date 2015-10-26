from TwitterAPI import TwitterAPI
import spotipy
from . alchemyapi import AlchemyAPI
from . import secrets
from .models import Tweet

api = TwitterAPI(secrets.TWITTER_CODES['CONSUMER_KEY'],
                 secrets.TWITTER_CODES['CONSUMER_SECRET'],
                 secrets.TWITTER_CODES['ACCESS_TOKEN'],
                 secrets.TWITTER_CODES['ACCESS_SECRET'])

def search(query):
    r = api.request('search/tweets', {'q': query, 'lang': 'en'})
    tweets = []
    text = []
    for tweet in r:
        date = format_date(tweet['created_at'])
        if tweet['text'] not in text:
            tweets.append({
                'date': date,
                'text': tweet['text']
            })
            text.append(tweet['text'])
    return tweets

def get_sentiment(tweets):
    sentiment_tweets = []
    for tweet in tweets:
        s = sentiment(tweet['text'])
        sentiment_tweets.append({
            'date': tweet['date'],
            'text': tweet['text'],
            'sentiment': s
        })
    return sentiment_tweets


def sentiment(tweet):
    alchemyapi = AlchemyAPI()
    alchemyapi.apikey = secrets.ALCHEMY_CODES[0]
    response = alchemyapi.sentiment('text', tweet)
    if response['docSentiment']['type'] == 'neutral':
        return 0
    return float(response['docSentiment']['score'])

def format_date(date):
    import dateutil.parser as parser
    date = parser.parse(date)
    return date.isoformat()

def easy_date(date):
    return ' '.join(date.ctime().split()[0:3])

def average_sentiment_per_day(tweets):
    sentiments = {}
    vals = {}
    for tweet in tweets:
        date = easy_date(tweet.pub_date)
        if date not in sentiments:
            sentiments[date] = tweet.sentiment
            vals[date] = 1
        else:
            sentiments[date] += tweet.sentiment
            vals[date] += 1
    for key in sentiments:
        sentiments[key] /= vals[key]
    return sentiments
