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

$ cd Documents
$ mkdir snowboy
$ cd snowboy
$ wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.0.tar.bz2
$ tar -xvf rpi-arm-raspbian-8.0-1.1.0.tar.bz2 
$ mv ./rpi-arm-raspbian-8.0-1.1.0/* ./.
$ python demo.py resources/snowboy.umdl

どばっとメッセージが出る。
最後に↓が表示されたら利用可能。

```
Listening... Press Ctrl+C to exit
```

マイクに向かって「snowboy」と呼びかける。

```
Listening... Press Ctrl+C to exit
INFO:snowboy:Keyword 1 detected at time: 2018-07-22 05:20:31
```

というメッセージが出ればテストOK。

### ビール、枝豆、などのpmdlファイルをsnowboyからダウンロード

### snowboydecorder.pyの上書き

### 動作確認
