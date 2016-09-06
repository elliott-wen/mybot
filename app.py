#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from jokes import Joker
from weathercn import WeatherCN
from weathernz import WeatherNZ
from newsfeed import NewsFeed
from videowaiter import VideoWaiter
class MyWXBot(WXBot):
    def __init__(self):
        super(MyWXBot, self).__init__()
        self.joker = Joker()
        self.weathernz = WeatherNZ()
        self.weathercn = WeatherCN()
        self.videowaiter = VideoWaiter()
        self.newsfeed = NewsFeed()
        self.cron_tasklist = [
            [self.weathernz, "Victoria", "20", 0, None],
            [self.weathercn, "Bitch", "00", 0, None],
            [self.newsfeed, "Victoria", "00", 0, None],
            [self.newsfeed, "Bitch", "00", 0, None]

        ]
        self.joke_word = [u'生气', u'哈', u'摸摸', u'哀家', u'小琪子', 'joke','angry',u'生气', u'无聊', 'boring','ha','lol']
        self.weather_word = ['weather', u'天气']
        self.news_word = [u'新闻','news']


    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 9:
            result = self.videowaiter.gen_message()
            if result is None:
                return
            self.send_img_msg_by_uid(result['pic'], msg['user']['id'])

        elif msg['msg_type_id'] == 4:
            data = msg['content']['data']
            for word in self.joke_word:
                if word in data:
                    result = self.joker.gen_message()
                    if result is None:
                        return
                    self.send_msg_by_uid(result['msg'], msg['user']['id'])
                    if 'pic' in result:
                        self.send_img_msg_by_uid(result['pic'], msg['user']['id'])
                    return

            for word in self.weather_word:
                if word in data:
                    result = self.weathernz.gen_message()
                    if result is None:
                        return
                    self.send_msg_by_uid(result['msg'], msg['user']['id'])
                    if 'pic' in result:
                        self.send_img_msg_by_uid(result['pic'], msg['user']['id'])
                    return

            for word in self.news_word:
                if word in data:
                    result = self.newsfeed.gen_message()
                    if result is None:
                        return
                    self.send_msg_by_uid(result['msg'], msg['user']['id'])
                    return




    def schedule(self):
        for task in self.cron_tasklist:
            #print "Handling Tasks %s %s"%(time.strftime("%H",time.gmtime()), task[2])
            if time.strftime("%H",time.gmtime()) == task[2] and time.time() - task[3] > 7200:
                print "Starting a cron job for %s"%task[1]
                result = task[0].gen_message(task[4])
                uid = self.get_user_id(task[1])
                if result is None:
                    continue
                self.send_msg_by_uid(result['msg'], uid)
                if 'pic' in result:
                    self.send_img_msg_by_uid(result['pic'], uid)
                task[3] = time.time()



def main():
    bot = MyWXBot()
    bot.DEBUG = False
    bot.run()


if __name__ == '__main__':
    main()
