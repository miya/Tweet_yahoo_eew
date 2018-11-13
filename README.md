# Tweet_yahoo_eew
[Yahoo地震情報](https://typhoon.yahoo.co.jp/weather/earthquake/)の更新をツイートするプログラム
## Setup
```git clone https://github.com/0x0u/Tweet_yahoo_eew.git```  

```pip3 install -r requiremenets.txt```  

```cd Tweet_yahoo_eew```  

エディターでtweet.pyを開きconsumer_key、consumer_secret、access_key、ccess_secretをそれぞれ自分のものに書き換える。  

```python3 main.py```
## Description
更新の有無はcheck.txtに震度画像のURLを書き込み、プログラムを起動するたびにcheck.txtを参照し以前の書き込みと同一だったら終了、更新があったらtweet関数を呼び出してツイートをします。 

## Sample
実際に動かしてみた → https://twitter.com/v0x0o  
RaspberryPiのcronで1分間隔でプログラムを起動し更新があったらツイートするアカウントとなっています。発生時刻、震源地、最大震度、マグニチュード、深さ、緯度経度、情報を震源地のイメージ画像とともにツイート、それに対して揺れた地域をスレッドとしてぶら下げます。    
<img src="https://i.imgur.com/rRE5ylI.png">

