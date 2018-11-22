import re
import sys
import requests
from bs4 import BeautifulSoup as bs

def data():
    url = 'https://typhoon.yahoo.co.jp/weather/jp/earthquake/'
    req = requests.get(url)
    soup = bs(req.content,'html.parser')
    info = [i.text for i in soup.find_all(width="70%")]
    pic = soup.find(id='earthquake-01').find('img').get('src')
    check(pic)
    get_pic(pic)
    text = '@test\n［test］\n・時刻: {}\n・震源地: {}\n・最大震度: {}\n・マグニチュード: {}\n・深さ: {}\n・緯度/経度: {}\n・情報: {}'.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6])
    geocode = [i for i in re.findall('\d*[.,]?\d*',info[5]) if i != '']
    gal = [i.text for i in soup.find_all(width="10%")]
    place = soup.find_all(width="90%")
    text2 = []
    for g,p in zip(gal,place):
        p = ''.join([i.text.replace('\u3000','、').replace('\n','') for i in p.find_all(width="99%")])
        p = p.strip('、')
        text2.append('《{}》 {:.135}'.format(g,p))
    return text,geocode,info[2],text2[::-1]

def get_pic(media_url):
    req = requests.get(media_url)
    with open('eew.png', 'wb') as w:
        w.write(req.content)

def check(text):
    with open('check.txt','r') as file1:
        t = file1.read()
    if text != t:
        print('update')
        with open('check.txt','w') as file2:
            file2.write(text)
    else:
        print('no update')
        sys.exit()
