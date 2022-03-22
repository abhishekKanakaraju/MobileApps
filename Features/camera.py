Skip to content

Please note that GitHub no longer supports your web browser.
We recommend upgrading to the latest Google Chrome or Firefox.
Ignore
Learn more

Search…
All gists
Back to GitHub
Sign up for a GitHub account Sign in
Instantly share code, notes, and snippets.
@susmit susmit/camera.py
Last active Feb 4, 2017
 Star 0  Fork 0
 Code  Revisions 1
Embed  
<script src="https://gist.github.com/susmit/91bebcc2d733dbfdc805ff333e5391d2.js"></script>
  Download ZIP
plyer linux camera feature
Raw
 camera.py
import subprocess as sb
from plyer.facades import Camera

class LinuxCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        #hardcoded filname for debuging process.
        sb.call([ "gst-launch" ,"v4l2src" ,"num-buffers=1", "!" ,"jpegenc" ,"!" ,"filesink" ,"location=/home/phunsukwangdu/Pictures/test.jpg" ])


    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        print("Feature under development")
        #most probably to be done with gstreamer-tools or streamer
        #streamer -q -c /dev/video0 -f rgb24 -r 3 -t 00:30:00 -o ~/outfile.avi


def instance():
    return LinuxCamera()
Sign up for free to join this conversation on GitHub. Already have an account? Sign in to comment
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
