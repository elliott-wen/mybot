#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from jokes import Joker
from weathercn import WeatherCN
from weathernz import WeatherNZ
class MyWXBot(WXBot):
    def __init__(self):
        super(MyWXBot, self).__init__()
        self.joker = Joker()
        self.weathernz = WeatherNZ()
        self.weathercn = WeatherCN()
        self.tasklist = [
            [self.weathernz, "Victoria", "11", 0],
            [self.weathercn, "Bitch", "0", 0]
        ]
        self.joke_word = [u'生气', u'哈', u'摸摸', u'哀家', u'小琪子', 'joke','angry',u'生气', u'无聊', 'boring','ha','lol']
        self.sing_word = [u'歌', 'sing', 'song']
        self.pending_msg = []


    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4:
            data = msg['content']['data']
            for word in self.joke_word:
                if word in data:
                    result = self.joker.gen_message()
                    if result == None:
                        return
                    self.send_msg_by_uid(result['msg'], msg['user']['id'])
                    if 'pic' in result:
                        self.send_img_msg_by_uid(result['pic'], msg['user']['id'])
                    return


    def schedule(self):
        for task in self.tasklist:
            if time.strftime("%H",time.gmtime()) == task[2] and time.time() - task[3] > 7200:
                print "Starting a cron job for %s"%task[1]
                result = task[0].gen_message()
                uid = self.get_user_id(task[1])
                if result == None:
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