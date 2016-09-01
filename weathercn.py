#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from plugin import *
import traceback
class WeatherCN(Plugin):

    def gen_message(self, caller_id = None, message = None):
        try:
            driver = webdriver.PhantomJS() # or add to your PATH
            driver.set_window_size(1024, 768) # optional
            driver.get('http://m.weathercn.com/index.do?id=101010100&partner=m')
            url = self.filename_generator("jpg")
            driver.save_screenshot(url) # save a screenshot to disk
            return {"msg":u"小琪子天气预报", "pic":url}
        except:
            traceback.print_exc()
            return None




