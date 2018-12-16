# Tweet_yahoo_eew
[Yahoo地震情報](https://typhoon.yahoo.co.jp/weather/earthquake/)の更新をツイートするプログラム
## Setup
```
git clone https://github.com/0x0u/Tweet_yahoo_eew.git  
pip3 install -r requiremenets.txt  
cd Tweet_yahoo_eew  
```  

エディターでEEW.pyを開きconsumer_key、consumer_secret、access_key、access_secretをそれぞれ自分のものに書き換える。  

## Description
更新の有無はcheck.txtに震度画像のURLを書き込み、プログラムを起動するたびにcheck.txtを参照し以前の書き込みと同一だったら終了、更新があったらtweetメソッドを呼び出してツイートをします。 

## Sample
実際に動かしてみた → https://twitter.com/v0x0o  
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
ツイート  
```Python
tweet_id = eew.tweet(text=data[0], lat=data[2][0], long_=data[2][1])
```
震度毎にスレッドツイート
```Python
for i in data[1]:
    tweet_id = eew.tweet(text=i, id_=tweet_id)
```


