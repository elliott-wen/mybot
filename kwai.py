import requests
import json
import time
import logging
import pymongo
from pymongo import MongoClient
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class KwaiDigger(object):

    def __init__(self):
        self.runningFlag = False
        self.dbclient = MongoClient()
        self.db = self.dbclient.kwai

    def retriveFeeds(self):

        param = {
        "os": "android",
                "client_key": "3c2cd3f3",
                "last": "347",
                "count": "20",
                "token": "",
                "page": "1",
                "pcursor": "",
               "pv": "false",
                "mtype": "2",
                "type": "7",
               "sig": "6ba9890fcd4ff34a3fe6624aa7099e8b"
        }
        r = requests.post("http://180.186.38.200/rest/n/feed/list?type=7&lat=31.239293&lon=121.683083&ver=4.40&ud=0&sys=ANDROID_4.4.4&c=360APP&oc=360APP&net=WIFI&did=ANDROID_f62f77bff70308a9&mod=Xiaomi%28MI+4LTE%29&app=0&language=zh-cn&country_code=CN&appver=4.40.0.750", param)
        data = json.loads(r.text)

        if data['result'] == 1:
            return data['feeds']
        else:
            return None

    def insert_to_database(self, record):
        #print "Inserting a record %s"%record['user_id']
        col = self.db.videos
        if col.count() > 4000:
            logging.debug( "Too much in database, cleaning")
            olds = col.find().sort("record_time", pymongo.ASCENDING).limit(20)
            for old in olds:
                col.remove({"_id": old["_id"]})
        if col.find_one({"user_id": record['user_id']}) is None:
            col.insert_one(record)



    def handleFeeds(self, feeds):
        for feed in feeds:
            if 'thumbnail_urls' not in feed or 'main_mv_urls' not in feed:
                continue
            thumburl = feed['thumbnail_urls'][0]['url']
            mv_url = feed['main_mv_urls'][0]['url']
            like_count = feed['like_count']
            user_id = feed['user_id']
            caption = feed['caption']
            video_time = feed['timestamp']
            view_count = feed['view_count']
            add_time = int(time.time())
            record = {"img_url":thumburl, "video_url":mv_url, "like_count": like_count, "view_count":view_count ,"user_id":user_id, "title": caption, "video_time": video_time, "record_time": add_time}
            self.insert_to_database(record)


    def run(self):
        self.runningFlag = True
        while self.runningFlag:
            logging.info("Fetching some new feeds")
            r = self.retriveFeeds()
            if r != None:
                self.handleFeeds(r)
                time.sleep(0.1)
            else:
                logging.error("Error when loading, sleep for a while")
                time.sleep(10)



k = KwaiDigger()
k.run()