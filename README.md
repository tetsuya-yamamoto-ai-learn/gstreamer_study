# RTSP配信・受信を行うサンプルプログラム

## 1. インストール

https://www.howtoinstall.me/ubuntu/18-04/gir1.2-gst-rtsp-server-1.0/

## 2. 受信コマンド

gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/stream1  ! decodebin ! videoconvert ! autovideosink