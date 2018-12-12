import re
import sys
import tweepy
import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon

class EEW:
    def init(self):
        pass

    def get_data(self):
        url = 'https://typhoon.yahoo.co.jp/weather/jp/earthquake/'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        info = [i.text for i in soup.find_all(width="70%")]
        image = soup.find(id='earthquake-01').find('img').get('src')
        self._check(text=image)
        self._get_image(image_url=image)
        text = '[地震速報]\n・時刻: {}\n・震源地: {}\n・最大震度: {}\n・マグニチュード: {}\n・深さ: {}\n・緯度/経度: {}\n・情報: {}'.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6])
        geocode = re.findall('\d+[.]+\d', info[5])
        place = soup.find_all(width="90%")[::-1]
        text2 = []
        for i in range(int(info[2])):
            p = '(.+?)\u3000'
            m = re.findall(p, str(place[i]))
            t = '、'.join(m)
            if len(t) >= 133:
                t = '{:.133}...'.format(t)
            text2.append('《震度{}》 {}'.format(i+1, t))
        return text, text2, geocode

    def _get_image(self, image_url):
        req = requests.get(image_url)
        with open('eew.png', 'wb') as w:
            w.write(req.content)

    def _check(self, text):
        with open('check.txt','r') as file1:
            t = file1.read()
        if text != t:
            print('update')
            with open('check.txt','w') as file2:
                file2.write(text)
        else:
            print('no update')
            sys.exit()

    def tweet(self, text, lat=None, long_=None, id_=None):
        consumer_key = 'consumer_key'
        consumer_secret = 'consumer_secret'
        access_key = 'access_key'
        access_secret = 'access_secret'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        if id_ == None:
            tweet = api.update_with_media(filename='eew.png', status=text, lat=lat, long=long_)
            return tweet.id
        if id_ != None:
            tweet = api.update_status(status=text, in_reply_to_status_id =id_)
            return tweet.id

    def toot(self, text, id_=None):
        mastodon = Mastodon(
        client_id="app_key.txt",
        access_token="user_key.txt",
        api_base_url = "https://pawoo.net")
        media_files = mastodon.media_post('eew.png', "image/png")
        if id_ == None:
            toot = mastodon.status_post(status=text, visibility='public', media_ids=media_files)
            return toot.id
        if id_ != None:
            toot = mastodon.status_post(status=text, visibility='public', in_reply_to_id=id_)
            return toot.id
