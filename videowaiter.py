import sys, urllib, urllib2, json
from plugin import Plugin
import traceback
import random

DATA_STORE = ["http://sd.keepcalm-o-matic.co.uk/i/keep-calm-i-m-busy.png",
              "http://sd.keepcalm-o-matic.co.uk/i/keep-calm-because-im-busy.png",
              "http://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-just-wait-167.png",
              "http://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-please-wait-38.png"
              ]

class VideoWaiter(Plugin):
    def gen_message(self, parameter = None):
        try:
            pic = random.randint(0, len(DATA_STORE)-1)
            download_url = self.filename_generator("jpg")
            urllib.urlretrieve(DATA_STORE[pic], download_url)
            return {"msg":"", "pic": download_url}
        except:
            traceback.print_exc()
            return None