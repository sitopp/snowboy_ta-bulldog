# snowboy_ta-bulldog


snowboyを、ta-bulldogにあわせてカスタマイズするためのコードです。


## 使用環境
- Raspberry Pi3
- USBマイク
  - 自分が使ってるもの）https://www.amazon.co.jp/gp/product/B003YUB660/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1


## 手順

- Raspberry Pi3にNoobsの最新版OSをインストールしておきます。
- Wi-fiあるいは有線LANでつなぎ、作業用のマシンからssh接続できるようにしておきます。
- Raspberry Pi3のIPアドレスは「192.168.0.13」として下記を記載しておりますが、環境にあわせて読み替えてください。

### ライブラリのインストール
```
$ sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
$ pip install pyaudio
$ sudo apt-get install libatlas-base-dev
```

### マイクデバイスの確認とasoundの設定

```
$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 7/7
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

$ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: U0x46d0x825 [USB Device 0x46d:0x825], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

```
スピーカーは、card 1,device 0
USBマイクは、card 1、device 0として認識されている。
そこで、asoundの設定を以下のようにする。

```
$ vi ~/.asoundrc
=====
pcm.!default {
  type asym
   playback.pcm {
     type plug
     slave.pcm "hw:0,0"
   }  
   capture.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
}
=====
```

### snowboyのダウンロードとテスト


```
$ cd Documents
$ wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.0.tar.bz2
$ tar -xvf rpi-arm-raspbian-8.0-1.1.0.tar.bz2 
```
「rpi-arm-raspbian-8.0-1.1.0」というディレクトリ名が長いので改名します
```
$ mv rpi-arm-raspbian-8.0-1.1.0 snowboy
$ cd snowboy
```
さっそくテスト実行します。
```
$ python demo.py resources/snowboy.umdl
```

最後に↓が表示されたら呼びかける準備ができてる。

```
Listening... Press Ctrl+C to exit
```

マイクに向かって「snowboy」と呼びかけ、以下のメッセージが出ればテストOK。

```
Listening... Press Ctrl+C to exit
INFO:snowboy:Keyword 1 detected at time: 2018-07-22 05:20:31
```


### ビール、枝豆、などのpmdlファイルをsnowboyからダウンロード

- ビール https://snowboy.kitt.ai/hotword/24457
- えだまめ https://snowboy.kitt.ai/hotword/24458
- 伏せ https://snowboy.kitt.ai/hotword/24461
- 戻って https://snowboy.kitt.ai/hotword/24460
- ストップ https://snowboy.kitt.ai/hotword/24459

![snowboy_download](https://user-images.githubusercontent.com/1670181/43042778-e2f9083e-8dbf-11e8-986a-af42b2f3bb25.png)

これらpmdlファイルを、Raspberry Pi3にアップロードする。

```
例）macの場合
　ターミナルから実行

$ cd 
$ cd Downloads
$ scp ./*.pmdl pi@192.168.0.13:/home/pi/Documents/snowboy/resources/.
```
### 動作確認

```
$ python demo.py resources/beer.pmdl
（中略）
Listening... Press Ctrl+C to exit
```

マイクに向かって「ビール」と呼びかけ、以下のメッセージが出ればテストOK。

```
INFO:snowboy:Keyword 1 detected at time: 日時
```

### snowboydecorder.pyのpatchあて


```
$ mkdir patch
$ cd patch
$ git clone https://github.com/sitopp/snowboy_ta-bulldog.git
$ cd snowboy_ta-bulldog/
$ cp ./snowboydecoder.py /home/pi/Documents/snowboy/.
$ cp ./stab.py /home/pi/Documents/snowboy/.
```
stab.pyは、正式なつなぎこみ先ができるまでのテスト用です。


### 動作確認

```
$ python demo.py resources/beer.pmdl
（中略）
Listening... Press Ctrl+C to exit
```

マイクに向かって「ビール」と呼びかけ、以下のメッセージが出ればテストOK。
最後に「INFO:snowboy:1」が出るところがキモ。

```
INFO:snowboy:Keyword 1 detected at time: 2018-07-22 06:03:06
INFO:snowboy:resources/beer.pmdl
INFO:snowboy:1
```

なお、「INFO:snowboy:1」の「1」は、ビールを表すパラメタです。
他に以下のバリエーションがあります。

```
1:ビール 
2:えだまめ
3:ふせ
4:戻って
5:ストップ
```
そこで、ちょっと面倒ですが、1個づつ起動して単体テストをします。

```
$ python demo.py resources/beer.pmdl  →「ビール」と発話し、判定ログがでることを確認したら、ctrl+c
$ python demo.py resources/edamame.pmdl  →「えだまめ」と発話し、判定ログがでることを確認したら、ctrl+c
$ python demo.py resources/fuse.pmdl  →「伏せ」と発話し、判定ログがでることを確認したら、ctrl+c
$ python demo.py resources/modotte.pmdl  →「戻って」と発話し、判定ログがでることを確認したら、ctrl+c
$ python demo.py resources/stop.pmdl  →「ストップ」と発話し、判定ログがでることを確認したら、ctrl+c
```
※「戻って」が反応しないとき、「戻れ」というとなぜか反応するときがあります。


## 起動について

Maker Faire Tokyoでは、上記5種類の「ホットワード」をTA-BULLDOGに認識させる予定です。<br>
以下のように5個のプロセスをnohupで立ち上げておきます。<br>

```
$ nohup python demo.py resources/beer.pmdl  >> detect_log &
$ nohup python demo.py resources/edamame.pmdl  >> detect_log &
$ nohup python demo.py resources/fuse.pmdl  >> detect_log &
$ nohup python demo.py resources/modotte.pmdl  >> detect_log &
$ nohup python demo.py resources/stop.pmdl  >> detect_log &
```
平行して5個立ち上げていると、認識のレスポンスが落ちて、発話してから認識完了まで1〜2秒かかることがあります。

プロセスを終了する時は、
```
ps -ax
（一覧）
kill プロセス番号
```
あるいは、RaspiをshutdownすればOK。

## 画像認識スクリプトの起動箇所

snowboydecoder.py の190〜200行めあたりに、stab.pyを呼び出している箇所があるので、
ここを画像認識スクリプトに書き換えてください。

```
request_string = "python /home/pi/Documents/snowboy/stab.py " + str(elem)
```
なおelemには前述の1〜5のパラメタが入りますので、画像認識スクリプトで使ってください。


## 補足
画像認識スクリプトがpython3環境なので、あわせてRaspberry Pi3にpython3.6をインストールし、snowboyを動かそうとしたのですが、依存関係が解消できず、暫定的に、stab.pyをpython3.6で起動するよう、修正しました。<br>


snowboydecoder.py　L.195
```
request_string = "python3.6 /home/pi/Documents/snowboy/stab.py " + str(elem)
```
