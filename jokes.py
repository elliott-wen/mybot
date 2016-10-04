#!/usr/bin/env python
# coding: utf-8
import random
import urllib2, json
import os
import urllib
from plugin import *
import traceback

class Joker(Plugin):

    def gen_message(self, parameter = None):
        if not self.quota_check():
            return None

        try:
            url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=hilarious'
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            content = resp.read()
            dic_str = json.loads(content)
            joke_str = u"笑话攻击"
            pic_url = dic_str['data']['fixed_height_downsampled_url']
            download_url = self.filename_generator("gif")
            if pic_url!='':
                urllib.urlretrieve(pic_url, download_url)
                pic_url = download_url
            return {"msg":joke_str, "pic":pic_url}
        except:
            traceback.print_exc()
            return None



