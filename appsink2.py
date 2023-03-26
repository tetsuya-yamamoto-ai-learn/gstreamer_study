## 目標
# pythonで砂嵐作成→パイプラインに流し込み→画面に表示(videosink)
# 参考　https://blog.csdn.net/zhoutianyou/article/details/123094941

import sys, os
import gi
import cv2
import time
import numpy as np
import datetime
gi.require_version("Gst", "1.0")
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib, GObject


def ndarray_to_gst_buffer(array: np.ndarray) -> Gst.Buffer:
    """Converts numpy array to Gst.Buffer"""
    return Gst.Buffer.new_wrapped(array.tobytes())


if __name__=='__main__':
    # 初期化
    Gst.init(None)
    
    # create pipeline
    pipeline = Gst.parse_launch(
        "appsrc name=src \
        ! video/x-raw,width=600,height=400,format=BGR,framerate=30/1 \
        ! videoconvert \
        ! autovideosink"
    )
    # pipeline = Gst.parse_launch(
    #     "appsrc name=src \
    #     ! video/x-raw,width=640,height=360,format=BGRx \
    #     ! videoconvert ! x264enc \
    #     ! rtph264pay config-interval=10 \
    #     ! udpsink host=127.0.0.1 port=9999"
    # )

    # pull appsrc element
    appsrc = pipeline.get_by_name("src")

    # pipline state set as PLAYING
    ret = pipeline.set_state(Gst.State.PLAYING)
    
    # push appsink
    while True:
        arr = np.random.randint(0, 255, (400, 600, 3), np.uint8)
        time_str = f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
        print(time_str, arr.shape)
        cv2.putText(arr, time_str, 
                    (100, 300), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=1, 
                    color=(0, 255, 0), 
                    thickness=2, 
                    lineType=cv2.LINE_4
        )
        appsrc.emit("push-buffer", ndarray_to_gst_buffer(arr))
        
        
