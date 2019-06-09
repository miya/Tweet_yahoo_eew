# Tweet_yahoo_eew
[Yahoo地震情報](https://typhoon.yahoo.co.jp/weather/earthquake/)の更新をツイートするプログラム
## Setup
```
$ git clone https://github.com/0x0u/Tweet_yahoo_eew.git  
$ pip3 install -r requiremenets.txt  
$ cd Tweet_yahoo_eew  
```  

エディターでeew.pyを開きconsumer_key、consumer_secret、access_key、access_secretをそれぞれ自分のものに書き換える。Mastodonで投稿する場合は

## Description
更新の有無はcheck.txtにYahoo地震情報トップ>履歴の最上部のhtmlをスクレイピングし発生時刻の数値をcheck.txtに書き込み、プログラムを起動するたびにcheck.txtを参照し以前の書き込みと同一だったら終了、更新があったらtweetメソッドを呼び出してツイートをします。 

## Sample
実際に動かしているアカウント  
Twitter: https://twitter.com/v0x0o  
Mastodon(Pawoo): https://pawoo.net/@eew

RaspberryPiのcronで1分間隔でプログラムを起動し更新があったらツイートするアカウントになっています。発生時刻、震源地、最大震度、マグニチュード、深さ、座標、地震情報を震源地のイメージ画像とともにツイート、それに対して揺れが観測された地域の情報をスレッドでぶら下げます。  

<img src="https://user-images.githubusercontent.com/34241526/59153916-3c724400-8aa1-11e9-904b-9939ea452cd3.png">

## How it works
setupを行うことでこのスクリプトを使うことが出来ます。

データ（ツイート用テキスト、揺れが観測された地域名、震源地のジオコード）の取得　　

```Python
data = eew.get_data()
```
dataを実際に出力するとこうなる
```
[地震速報]
・時刻: 2019年5月12日 15時07分ごろ
・震源地: 日向灘v
・最大震度: 3
・マグニチュード: 4.3
・深さ: 30km
・緯度/経度: 北緯32.7度/東経132.3度
・情報: この地震による津波の心配はありません。
['《震度1》 伊方町、松野町、愛媛鬼北町、土佐清水市、黒潮町、神埼市、西原村、山都町、大分市、臼杵市、日向市、宮崎美郷町', '《震度2》 宇和島市、西予市、愛南町、大月町、阿蘇市、産山村、熊本高森町、佐伯市、津久見市、竹田市、豊後大野市、延岡市、高千穂町', '《震度3》 宿毛市']
['32.7', '132.3']
```
ツイート（Twitter）
```Python
twitter = twitter_api()
tweet_id = tweet(twitter, text=data[0], lat=data[2][0], lon=data[2][1])
```
震度毎にスレッドツイート
最初に上記のツイートを行う必要がある

```Python
for i in data[1]:
    tweet_id = tweet(twitter, text=i, id_=tweet_id)
```

トゥート（Mastodon）
```python
mastodon = mastodon_api()
toot_id = toot(mastodon, text=data[0])
for i in data[1]:
    tweet_id = tweet(twitter, text=i, id_=tweet_id)
    toot_id = toot(mastodon, text=i, id_=toot_id)
```


