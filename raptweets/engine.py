from TwitterAPI import TwitterAPI
import spotipy

from . alchemyapi import AlchemyAPI
from . import secrets

from .models import Tweet, Album


api = TwitterAPI(secrets.TWITTER_CODES['CONSUMER_KEY'],
                 secrets.TWITTER_CODES['CONSUMER_SECRET'],
                 secrets.TWITTER_CODES['ACCESS_TOKEN'],
                 secrets.TWITTER_CODES['ACCESS_SECRET'])

# TODO more relevant tweets
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
    if response['status'] == 'ERROR':
        return 0
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

# TODO more intelligent spotify queries -- perhaps add more search fields *shudder*
def spotify_search(query):
    sp = spotipy.Spotify()
    result = sp.search(q=query, limit=1)
    if not result['tracks']['items']:
        return None
    try:
        title = format_title(result['tracks']['items'][0]['album']['name'])
        artist = result['tracks']['items'][0]['artists'][0]['name']  # get first listed artist
        return title, artist
    except KeyError:
        return None

def search_and_add_tweets(album):
    query = get_sentiment(search(album.title))
    for tweet in query:
        t = Tweet(text=tweet['text'],
                  sentiment=tweet['sentiment'],
                  pub_date=tweet['date'],
                  album=album)
        try:
            Tweet.objects.get(text=t.text)
        except(KeyError, Tweet.DoesNotExist):
            t.save()

def format_title(title):
    low = title.split()
    fluff = [
        '(Explicit',
        'Version)',
        '(Deluxe',
        'Explicit',
        'Eeluxe)',
        'Deluxe',
        '[Deluxe',
        'Edition(Explicit)]',
        '(Deluxe)',
        'Edition]',
        '[Platinum',
        '(Remastered)',
        'Remaster)',
        '(2002',
        '(2011',
        '-',
        '(Legacy'
    ]
    for word in fluff:
        if word in low:
            low.remove(word)
    return ' '.join(low)

def close_titles():
    titles = {}
    a = Album.objects.all()
    for i in range(len(a)):
        titles[a[i].title.lower()] = a[i]
    return titles
