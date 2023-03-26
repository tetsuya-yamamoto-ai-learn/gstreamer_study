## 目標
# pythonで砂嵐作成→パイプラインに流し込み→画面に表示(videosink)
# 参考　https://blog.csdn.net/zhoutianyou/article/details/123094941

import sys, os
import gi
import cv2
import time
import numpy as np
gi.require_version("Gst", "1.0")
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib, GObject


def ndarray_to_gst_buffer(array: np.ndarray) -> Gst.Buffer:
    """Converts numpy array to Gst.Buffer"""
    return Gst.Buffer.new_wrapped(array.tobytes())


if __name__=='__main__':
    # 初期化
    Gst.init(None)
    
    pipeline_str = \
        "appsrc name=src \
        ! video/x-raw,width=640,height=360,format=BGRx \
        ! videoconvert \
        ! video/x-raw,format=I420 \
        ! x264enc \
        ! rtph264pay name=pay0 config-interval=1 pt=96"
    pipeline = Gst.parse_launch(pipeline_str)
        
    # pull appsrc element
    appsrc = pipeline.get_by_name("src")

    # add rtsp server element
    server = GstRtspServer.RTSPServer.new()
    server.set_service(str("5050"))
    mounts = server.get_mount_points()
    factory = GstRtspServer.RTSPMediaFactory.new()
    factory.set_launch(pipeline_str)
    factory.set_shared(True)
    mounts.add_factory('/test', factory)
    
    # start main loop
    loop = GLib.MainLoop()
    loop.run()
    
    # # pipline state set as PLAYING
    # ret = pipeline.set_state(Gst.State.PLAYING)
    
    while True:
        arr = np.random.randint(low=0, high=255, size=(640, 360, 4), dtype=np.uint8)
        appsrc.emit("push-buffer", ndarray_to_gst_buffer(arr))
        
