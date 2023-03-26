## 目標
# pythonで砂嵐作成→パイプラインに流し込み→画面に表示(videosink)

import sys, os
import gi
import cv2
import time
import numpy as np
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib, GObject


def ndarray_to_gst_buffer(array: np.ndarray) -> Gst.Buffer:
    """Converts numpy array to Gst.Buffer"""
    return Gst.Buffer.new_wrapped(array.tobytes())


if __name__=='__main__':
    # 初期化
    # GObject.threads_init()
    Gst.init()
    
    # パイプラインの作成
    print("Creating pipeline...")
    pipeline = Gst.Pipeline()
    if not pipeline:
        sys.stderr.write('Unable to create Pipeline')
        
    # Source element for reading from the file
    print("Creating Source")
    # appsrc
    appsource = Gst.ElementFactory.make("appsrc", "e-appsrc")
    # video converter
    videoconvert = Gst.ElementFactory.make("videoconvert", "e-videoconvert")
    # autovideosink
    autovideosink = Gst.ElementFactory.make("autovideosink", "e-autovideosink")

    # create caps
    caps_in = Gst.Caps.from_string("video/x-raw,format=RGBA,width=640,height=480,framerate=30/1")
    caps = Gst.Caps.from_string("video/x-raw,format=I420")
    appsource.set_property('caps', caps_in)
    # videoconvert.set_property('caps', caps)
    # caps_in = Gst.Caps.from_string("video/x-raw,format=RGBA,width=640,height=480,framerate=30/1")
    
    # Linking element
    appsource.link(videoconvert)
    videoconvert.link(autovideosink)
    
    # create an event loop and feed gstreamer bus mesages to it
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    # bus.connect("message", bus_call, loop)

    # start play back and listen to events
    print("Starting pipeline")
    pipeline.set_state(Gst.State.PLAYING)
    
    # Push buffer and check
    for _ in range(10):
        arr = np.random.randint(low=0,high=255,size=(480,640,3),dtype=np.uint8)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGBA)
        appsource.emit("push-buffer", ndarray_to_gst_buffer(arr))
        time.sleep(0.3)
    appsource.emit("end-of-stream")
    try:
        loop.run()
    except:
        pass
    # cleanup
    pipeline.set_state(Gst.State.NULL)    
    

    # if not appsource:
    #     sys.stderr.write(" Unable to create Source")

    pass
    # playerの作成
    # player = Gst.Pipeline.new("player")
    
    # pipelineの作成
    # pipeline = Gst.parse_launch("appsrc ! x264enc ! autovideosink")
    
    # # elementの作成
    # source = Gst.ElementFactory.make("file", "e-filesrc")
    # demux = Gst.ElementFactory.make("qtdemux", "e-qtdemux")
    # h264parser = Gst.ElementFactory.make("h264parse", "e-h264parse")
    # decoder = Gst.ElementFactory.make("decodebin", "e-decodebin")
    # h264encoder = Gst.ElementFactory.make("x264enc", "e-x264enc")
    # rtph264pay = Gst.ElementFactory.make("rtph264pay", "e-rtph264pay")