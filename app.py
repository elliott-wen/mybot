#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from jokes import Joker
from weathercn import WeatherCN
from weathernz import WeatherNZ
from newsfeed import NewsFeed
from dynamictext import DynamicText
import ConfigParser
import sqlite3
class MyWXBot(WXBot):


    joke_word = [u'生气', u'哈', u'摸摸', u'哀家', u'小琪子', 'Joke','angry',u'生气', u'无聊', 'boring','ha','lol',u'笑话','joke']
    weather_word = ['weather', u'天气']
    news_word = [u'新闻','news']
    barrage_word = [u'弹幕', 'barrage', 'bar', 'Bar']


    def __init__(self):
        super(MyWXBot, self).__init__()
        self.tuling_key = ""
        self.sqlconn = None
        self.robot_switch = False
        self.joker = Joker()
        self.weathernz = WeatherNZ()
        self.weathercn = WeatherCN()
        self.newsfeed = NewsFeed()
        self.texter = DynamicText()
        self.cron_tasklist = [
            [self.weathernz, "Victoria", "10", 0, None],
            [self.newsfeed, "Victoria", "00", 0, None],
        ]

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('config.ini')
            self.tuling_key = cf.get('main', 'key')
            print "Using the key " + self.tuling_key
        except Exception:
            print "Unable to load key!"


        try:
            self.sqlconn = sqlite3.connect("record.db")
        except Exception:
            print "Unable to connect database"


    def tuling_auto_reply(self, uid, msg):
        if not self.tuling_key:
            return None
        try:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " + k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
            return {"msg": u"小琪子:"+ result}
        except:
            traceback.print_exc()
            return None

    def auto_switch(self, data, uid):
        msg_data = data
        stop_cmd = [u'芝麻关门']
        start_cmd = [u'芝麻开门']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[小琪子，喳！]', uid)
                    return True
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[小琪子，喳！]', uid)
                    return True
        return False



    @override
    def handle_msg_all(self, msg):
        # if not self.robot_switch and msg['msg_type_id'] != 1:
        #     return

        if msg['msg_type_id'] != 1 and msg['msg_type_id'] != 4:
            #print "Ignore the message whose type is not 1 and 4"
            return


        if msg['content']['type'] != 0:
            #print "Ignore non-text message"
            return



        data = msg['content']['data']
        uid = ''
        if msg['msg_type_id'] == 1:
            uid = msg['to_user_id']
        else:
            uid = msg['user']['id']
        displayname = msg['user']['name']

        if self.sqlconn is not None:
            try:
                c = self.sqlconn.cursor()
                c.execute('''insert into records (username, record_text, record_date) values(?, ?, ? )''', (displayname, data, int(time.time())))
                self.sqlconn.commit()
            except:
                traceback.print_exc()
                print "Unable to write database"

        for word in self.barrage_word:
            if data.startswith(word):
                str = data[len(word):]
                if str == "":
                    return
                result = self.texter.gen_message(str)
                if result == None:
                    return
                if 'pic' in result:
                    self.send_img_msg_by_uid(result['pic'], uid)
                return

        if self.auto_switch(data, uid):
            return



        for word in self.joke_word:
            if word in data:
                result = self.joker.gen_message()
                if result is None:
                    return
                #self.send_msg_by_uid(result['msg'], uid)
                if 'pic' in result:
                    self.send_img_msg_by_uid(result['pic'], uid)
                return

        for word in self.weather_word:
            if word in data:
                result = self.weathernz.gen_message()
                if result is None:
                    return
                self.send_msg_by_uid(result['msg'], uid)
                if 'pic' in result:
                    self.send_img_msg_by_uid(result['pic'], uid)
                return

        for word in self.news_word:
            if word in data:
                result = self.newsfeed.gen_message()
                if result is None:
                    return
                self.send_msg_by_uid(result['msg'], uid)
                return

        if not self.robot_switch:
            return

        if msg['msg_type_id'] == 4:
            print "Passing bot for message handling"
            bot_result = self.tuling_auto_reply(uid, data)
            if bot_result is not None:
                self.send_msg_by_uid(bot_result["msg"], uid)





    #
    # def handle_msg_all(self, msg):
    #     print "Handling a msg with %d"%(msg['msg_type_id'])
    #
    #
    #     if msg['msg_type_id'] == 4:
    #         # if msg['content']['type'] == 8 or msg['content']['type'] == 9:
    #         #     result = self.videowaiter.gen_message()
    #         #     if result is None:
    #         #         return
    #         #     self.send_img_msg_by_uid(result['pic'], msg['user']['id'])
    #         #     return
    #
    #
    #
    #
    #
    #
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
