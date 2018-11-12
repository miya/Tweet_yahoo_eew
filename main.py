import tweet
from get_data import data

if __name__ == '__main__':
    data = data()
    id_ = tweet.tweet(data[0],lat=data[1][0],long_=data[1][1])
    for i in data[3]:
        tweet.tweet(i,id_=id_)

