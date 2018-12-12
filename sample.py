from EEW import EEW

eew = EEW()
data = eew.get_data()

tweet_id = eew.tweet(text=data[0], lat=data[2][0], long_=data[2][1])
toot_id = eew.toot(text=data[0])

for i in data[1]:
    tweet_id = eew.tweet(text=i, id_=tweet_id)
    toot_id = eew.toot(i, id_=toot_id)
