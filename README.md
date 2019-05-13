# Tweet_yahoo_eew
[Yahoo地震情報](https://typhoon.yahoo.co.jp/weather/earthquake/)の更新をツイートするプログラム
## Setup
```
$ git clone https://github.com/0x0u/Tweet_yahoo_eew.git  
$ pip3 install -r requiremenets.txt  
$ cd Tweet_yahoo_eew  
```  

エディターでEEW.pyを開きconsumer_key、consumer_secret、access_key、access_secretをそれぞれ自分のものに書き換える。  

## Description
更新の有無はcheck.txtに震度画像のURLを書き込み、プログラムを起動するたびにcheck.txtを参照し以前の書き込みと同一だったら終了、更新があったらtweetメソッドを呼び出してツイートをします。 

## Sample
実際に動かしているアカウント  
Twitter: https://twitter.com/v0x0o  
Mastodon(Pawoo): https://pawoo.net/@eew

RaspberryPiのcronで1分間隔でプログラムを起動し更新があったらツイートするアカウントになっています。発生時刻、震源地、最大震度、マグニチュード、深さ、座標、地震情報を震源地のイメージ画像とともにツイート、それに対して揺れが観測された地域の情報をスレッドでぶら下げます。  

<img src="https://i.imgur.com/rRE5ylI.png">

## How to use
setupを行いsample.pyを実行すれば地震情報がツイートできます。

別ファイルから読み込む場合はインポートする  
```Python
from EEW import EEW
```
インスタンスの作成  
```Python
eew = EEW()
```
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

ツイート  
```Python
tweet_id = eew.tweet(text=data[0], lat=data[2][0], long_=data[2][1])
```
震度毎にスレッドツイート
```Python
for i in data[1]:
    tweet_id = eew.tweet(text=i, id_=tweet_id)
```


