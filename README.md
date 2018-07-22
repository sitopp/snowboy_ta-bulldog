# snowboy_ta-bulldog


snowboyを、ta-bulldogにあわせてカスタマイズするためのコードです。


## 使用環境
- Raspberry Pi3
- USBマイク
  - 自分が使ってるもの）https://www.amazon.co.jp/gp/product/B003YUB660/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1


## 手順


### ライブラリのインストール

$ sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
$ pip install pyaudio
$ sudo apt-get install libatlas-base-dev


### マイクデバイスの確認とasoundの設定

```
$ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: U0x46d0x825 [USB Device 0x46d:0x825], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

```

USBマイクは、card 1、device 0として認識されている。
そこで、asoundの設定を以下のようにする。

```
$ vi ~/.asoundrc
=====
pcm.!default {
  type asym
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
$ mkdir snowboy
$ cd snowboy
$ wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.0.tar.bz2
$ tar -xvf rpi-arm-raspbian-8.0-1.1.0.tar.bz2 
$ mv ./rpi-arm-raspbian-8.0-1.1.0/* ./.
$ python demo.py resources/snowboy.umdl
```

どばっとメッセージが出る。
最後に↓が表示されたら利用可能。

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

```
INFO:snowboy:Keyword 1 detected at time: 2018-07-22 06:03:06
INFO:snowboy:resources/beer.pmdl
INFO:snowboy:1
```

なお、最後の「INFO:snowboy:1」の「1」は、ビールを表すパラメタです。
ほかに以下のバリエーションがあります。

```
1:ビール 
2:えだまめ
3:ふせ
4:戻って
5:ストップ
```

