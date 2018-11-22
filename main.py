import tweet
from get_data import data

if __name__ == '__main__':
    data = data()
    tweet_id = tweet.tweet(data[0],lat=data[1][0],long_=data[1][1])
    toot_id = tweet.toot(data[0])
    for i in data[3]:
        tweet_id = tweet.tweet(i,id_=tweet_id)
        toot_id = tweet.toot(i,id_=toot_id)
