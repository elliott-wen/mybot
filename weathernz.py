from selenium import webdriver
from plugin import *
import traceback


class WeatherNZ(Plugin):
    def gen_message(self, caller_id = None, message = None):
        try:
            driver = webdriver.PhantomJS() # or add to your PATH
            driver.set_window_size(1024, 768) # optional
            driver.get('http://www.metservice.com/towns-cities/wellington/wellington-city')
            url = self.filename_generator("jpg")
            driver.save_screenshot(url) # save a screenshot to disk
            return {"msg":"Weather Forecast", "pic":url}
        except:
            traceback.print_exc()
            return None

