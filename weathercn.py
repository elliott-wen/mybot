#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from plugin import *
import traceback
from PIL import Image
class WeatherCN(Plugin):

    def gen_message(self, parameter = None):
        try:
            driver = webdriver.PhantomJS() # or add to your PATH
            driver.set_window_size(1024, 768) # optional
            driver.get('http://m.weathercn.com/index.do?id=101010100&partner=m')
            url = self.filename_generator("jpg")
            driver.save_screenshot(url) # save a screenshot to disk
            section = driver.find_element_by_css_selector("div.header-info")
            l =  section.location

            r = [l['x'], l['y'], 1000, 1300]
            im = Image.open(url)
            region = im.crop(r)
            non_transparent=Image.new('RGBA',region.size,(255,255,255,255))
            non_transparent.paste(region,(0,0),region)
            non_transparent.save(url)
            return {"msg":u"小琪子天气预报", "pic":url}
        except:
            traceback.print_exc()
            return None


# WeatherCN().gen_message()
#
