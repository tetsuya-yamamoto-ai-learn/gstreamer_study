
#  Copyright (C) 2020 Matteo Benedetto <me at enne2.net>
import gi
import numpy as np
from multiprocessing import Process
import datetime
import cv2
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GObject, GstRtspServer


def ndarray_to_gst_buffer(array: np.ndarray) -> Gst.Buffer:
    """Converts numpy array to Gst.Buffer"""
    return Gst.Buffer.new_wrapped(array.tobytes())


class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def init(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)
    
    def do_create_element(self, url):
        print('create pipeline')
        pipeline_str = \
            "appsrc name=src is-live=true size=1000000000 \
            ! video/x-raw,width=600,height=400,format=BGR \
            ! videoconvert \
            ! video/x-raw,format=I420 \
            ! x264enc \
            ! rtph264pay name=pay0"
        # pipeline_str = \
        #     "videotestsrc is-live=True pattern=ball animation-mode=1 \
        #     ! videoconvert \
        #     ! video/x-raw,format=I420 \
        #     ! x264enc \
        #     ! rtph264pay name=pay0"
        pipeline = Gst.parse_launch(pipeline_str)
        # pull appsrc element
        self.appsrc = pipeline.get_by_name("src")
        p = Process(target=self.update_image_process)
        p.start()
        return pipeline
    
    def update_image_process(self):
        # push appsink
        print('start update image process')
        while True:
            if self.appsrc is not None:
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
                self.appsrc.emit("push-buffer", ndarray_to_gst_buffer(arr))       
            else:
                pass
            

if __name__=='__main__':
    Gst.init(None)
    loop = GLib.MainLoop()

    port = "5050"
    mount_point = "/test"

    server = GstRtspServer.RTSPServer()
    server.set_service(port)
    mounts = server.get_mount_points()
    factory = TestRtspMediaFactory()
    factory.set_shared(True)
    mounts.add_factory(mount_point, factory)
    server.attach()

    #  start serving
    print ("stream ready at rtsp://127.0.0.1:" + port + "/test");
    loop.run()