
#  Copyright (C) 2020 Matteo Benedetto <me at enne2.net>
import gi
import numpy as np
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
        
        pipeline = Gst.parse_launch(pipeline)
        
        return 

Gst.init(None)

port = "5050"
mount_point = "/test"

# pipeline_str = \
#     "videotestsrc is-live=True pattern=ball animation-mode=1 \
#     ! videoconvert \
#     ! theoraenc \
#     ! queue \
#     ! rtptheorapay name=pay0"
pipeline_str = \
    "videotestsrc is-live=True pattern=ball animation-mode=1 \
    ! videoconvert \
    ! video/x-raw,format=I420 \
    ! x264enc \
    ! rtph264pay name=pay0"
# pipeline_str = \
#     "appsrc name=src is-live=True do-timestamp=True \
#     ! video/x-raw,width=640,height=360,format=BGRx \
#     ! videoconvert \
#     ! video/x-raw,format=I420 \
#     ! x264enc \
#     ! rtph264pay name=pay0 config-interval=1 pt=96"

server = GstRtspServer.RTSPServer.new()
server.set_service(port)
mounts = server.get_mount_points()
factory = GstRtspServer.RTSPMediaFactory.new()
factory.set_launch(pipeline_str)
mounts.add_factory(mount_point, factory)
server.attach()

#  start serving
print ("stream ready at rtsp://127.0.0.1:" + port + "/test");
loop = GLib.MainLoop()
loop.run()

# # push appsink
# while True:
#     arr = np.random.randint(0, 255, (400, 600, 3), np.uint8)
#     time_str = f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
#     print(time_str, arr.shape)
#     cv2.putText(arr, time_str, 
#                 (100, 300), 
#                 fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
#                 fontScale=1, 
#                 color=(0, 255, 0), 
#                 thickness=2, 
#                 lineType=cv2.LINE_4
#     )
#     appsrc.emit("push-buffer", ndarray_to_gst_buffer(arr))
    
        
