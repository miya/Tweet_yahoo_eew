import tweepy

def tweet(text,lat=None,long_=None,id_=None):
    consumer_key = 'consumer_key'
    consumer_secret = 'consumer_secret'
    access_key = 'access_key'
    access_secret = 'access_secret'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    if id_ == None:
        tweet = api.update_with_media(filename='eew.png',status=text,lat=lat,long=long_)
        return tweet.id
    if id_ != None:
        tweet = api.update_status(status=text,in_reply_to_status_id =id_)
        return tweet.id
