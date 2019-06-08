import re
import sys
import tweepy
import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon


"""
ここでTwitter及びMastodonに投稿するための
データ（時刻、震源地、祭壇震度、マグニチュード、深さ、座標、津波などの情報、揺れた地域）を取得する
"""
def get_data():
    url = 'https://typhoon.yahoo.co.jp/weather/jp/earthquake/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    info = [i.text for i in soup.find_all(width="70%")]
    image = soup.find(id='earthquake-01').find('img').get('src')
    check(text=image)
    get_image(image_url=image)
    text = '[地震速報]\n・時刻: {}\n・震源地: {}\n・最大震度: {}\n・マグニチュード: {}\n・深さ: {}\n・緯度/経度: {}\n・情報: {}'.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6])
    geocode = re.findall('\d+[.]+\d', info[5])
    place = soup.find_all(width="90%")[::-1]
    text2 = []
    intensity = int(re.findall('\d+', info[2])[0])
    for i in range(intensity):
        p = '、'.join(re.findall('(.+?)\u3000', str(place[i])))
        if len(p) >= 133:
            p = '{:.133}...'.format(p)
        text2.append('《震度{}》 {}'.format(i+1, p))
    return text, text2, geocode
    
# 画像保存用メソッド
"""
地震情報の画像をダウンロードし保存する
"""
def get_image(image_url):
    req = requests.get(image_url)
    with open('eew.png', 'wb') as w:
        w.write(req.content)


# 更新チェックメソッド
"""
更新の有無を確認するためのもの
地震情報の画像URLをcheck.txtに書き込み、cronなどで定期実行した際に
同一のURLだったらプログラム終了、違っていたら続行とする
"""
def check(text):
    with open('check.txt','r') as file1:
        t = file1.read()
    if text != t:
        print('更新があります')
        with open('check.txt','w') as file2:
            file2.write(text)
    else:
        print('更新がありません')
        sys.exit()

# Twitter API
def twitter_api():
    consumer_key = 'consumer_key'
    consumer_secret = 'consumer_secret'
    access_key = 'access_key'
    access_secret = 'access_secret'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api

# Tweet用メソッド
def tweet(text, lat=None, lon=None, id_=None):
    api = twitter_api()
    if id_ == None:
        tweet = api.update_with_media(filename='eew.png', status=text, lat=lat, long=lon)
        return tweet.id
    elif id_ != None:
        tweet = api.update_status(status=text, in_reply_to_status_id =id_)
        return tweet.id

# Mastodon API
def mastodon_api():
    mastodon = Mastodon(
    client_id="app_key.txt",
    access_token="user_key.txt",
    api_base_url = "https://pawoo.net")
    return mastodon

# Toot用メソッド
def toot(text, id_=None):
    mastodon = mastodon_api()
    media_files = mastodon.media_post('eew.png', "image/png")
    if id_ == None:
        toot = mastodon.status_post(status=text, visibility='direct', media_ids=media_files)
        return toot.id
    elif id_ != None:
        toot = mastodon.status_post(status=text, visibility='direct', in_reply_to_id=id_)
        return toot.id