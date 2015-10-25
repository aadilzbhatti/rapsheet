from TwitterAPI import TwitterAPI
from . alchemyapi import AlchemyAPI
from . import secrets

api = TwitterAPI(secrets.TWITTER_CODES['CONSUMER_KEY'],
                 secrets.TWITTER_CODES['CONSUMER_SECRET'],
                 secrets.TWITTER_CODES['ACCESS_TOKEN'],
                 secrets.TWITTER_CODES['ACCESS_SECRET'])

def search(query):
    r = api.request('search/tweets', {'q': query})
    tweets = []
    for tweet in r:
        date = format_date(tweet['created_at'])
        tweets.append({
            'date': date,
            'text': tweet['text']
        })
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
