import cv2
import numpy

# 参考
# https://fumimaker.net/entry/2022/07/17/231342
# https://teratail.com/questions/1dty42nhbtfw6s

# out = cv2.VideoWriter(
#     'appsrc ! videoconvert ! videoscale ! video/x-raw,format=I420 ! v4l2sink device=/dev/video42',
#     0,           # 出力形式。今回は0で。
#     30,          # FPS
#     (320, 240),  # 出力画像サイズ
#     True,        # カラー画像フラグ
# )

out = cv2.VideoWriter(
    # 'appsrc ! jpegenc ! image/jpeg, mapping=/stream !  udpsink rtsp://127.0.0.1:12345/stream1',
    'appsrc ! videoconvert ! video/x-raw,format=I420 ! autovideosink',
    0,           # 出力形式。今回は0で。
    30,          # FPS
    (320, 240),  # 出力画像サイズ
    True,        # カラー画像フラグ
)

while cv2.waitKey(1) != 27:
    img = numpy.random.randint(0, 255, (240, 320, 3), numpy.uint8)  # いわゆる砂嵐画像を生成
    # cv2.imshow('preview', img)
    out.write(img)