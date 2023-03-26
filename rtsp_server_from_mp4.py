#!/usr/bin/env python

# client
# gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/stream1  ! decodebin ! videoconvert ! autovideosink

import os
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

loop = GLib.MainLoop()
Gst.init(None)

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        # #set mp4 file path to filesrc's location property
        # src_demux = "filesrc location=videos/{} !".format(src_file)
        # # h264_transcode = "demux.video_0"
        # #uncomment following line if video transcoding is necessary
        # h264_transcode = "decodebin ! queue ! x264enc"
        # pipeline = "{0} {1} ! queue ! rtph264pay name=pay0 config-interval=1 pt=96".format(src_demux, h264_transcode)
        pipeline = 'filesrc location=data/sample.mp4 ! qtdemux ! h264parse ! decodebin ! videoconvert ! x264enc bitrate=16000000 ! rtph264pay name=pay0 config-interval=1 pt=96'
        print ("Element created: " + pipeline)
        return Gst.parse_launch(pipeline)

class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory('/{}'.format(dst_stream), factory)
        print(dir(mountPoints))
        self.rtspServer.attach(None)

if __name__ == '__main__':
    src_file = 'data/sample.mp4'
    dst_stream = 'stream1'
    s = GstreamerRtspServer()
    loop.run()
