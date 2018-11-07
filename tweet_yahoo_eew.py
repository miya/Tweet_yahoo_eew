import requests,tweepy,sys,re
from bs4 import BeautifulSoup as bs


def main():
    url = 'https://typhoon.yahoo.co.jp/weather/jp/earthquake/'
    req = requests.get(url)
    soup = bs(req.content,'html.parser')
    info = [i.text for i in soup.find_all(width="70%")]
    pic = soup.find(id='earthquake-01').find('img').get('src')
    check(pic)
    text = '［地震速報］#jishin \n・時刻: {}\n・震源地: {}\n・最大震度: {}\n・マグニチュード: {}\n・深さ: {}\n・緯度/経度: {}\n・情報: {}\n'.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6])
    geocode = [i for i in re.findall('\d*[.,]?\d*',info[5]) if i != '']
    get_pic(pic)
    tweet(text,geocode[0],geocode[1])


def get_pic(media_url):
    req = requests.get(media_url)
    with open('eew.png', 'wb') as w:
        w.write(req.content)


def check(text):
    with open('data.txt','r') as file1:
        t = file1.read()
    if text != t:
        print('update')
        with open('data.txt','w') as file2:
            file2.write(text)
    else:
        print('no update')
        sys.exit()

def tweet(text,lat,long_):
    consumer_key = 'your_comsumer_key'
    consumer_secret = 'your_consumer_secret'
    access_key = 'your_access_key'
    access_secret = 'your_access_secret'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    data = api.update_with_media(filename='eew.png',status=text,lat=lat,long=long_)


if __name__ == '__main__':
    main()
