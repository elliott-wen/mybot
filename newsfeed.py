
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json
from plugin import Plugin
import random
import traceback
class NewsFeed(Plugin):

    def gen_message(self, parameter = None):
        try:
            url = 'http://apis.baidu.com/txapi/huabian/newtop?num=10&page=%d'%random.randint(1,50)
            req = urllib2.Request(url)
            req.add_header("apikey", "77a27415631d269a2be4a40e388f5122")
            resp = urllib2.urlopen(req)
            content = resp.read()
            data = json.loads(content)
            articles = data['newslist']
            finalStr = ""
            for art in articles:
                finalStr += (art['title'] + '\n')
                finalStr += (art['url'] + '\n')
            #print finalStr
            return {"msg":finalStr}
        except:
            traceback.print_exc()
            return None


