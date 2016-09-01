#!/usr/bin/env python
# coding: utf-8
import random
import urllib2, json
import os
import urllib
from plugin import *
import traceback

class Joker(Plugin):

    def gen_message(self, caller_id = None, message = None):
        if not self.quota_check():
            return None
        page = random.randint(1,3800)
        try:
            url = 'http://api.1-blog.com/biz/bizserver/xiaohua/list.do?size=5&page=%d'%page
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            content = resp.read()
            dic_str = json.loads(content)
            joke_str = ""
            pic_url = ""
            for i in range(5):
                joke_str = u"小琪子:" + dic_str['detail'][i]['content'] + '\n';
                pic_url = dic_str['detail'][i]['picUrl']
                if pic_url != '':
                    break
            download_url = self.filename_generator("jpg")
            if pic_url!='':
                urllib.urlretrieve(pic_url, download_url)
                pic_url = download_url
            return {"msg":joke_str, "pic":pic_url}
        except:
            traceback.print_exc()
            return None

