from selenium import webdriver
from plugin import *
import traceback
from PIL import Image

class WeatherNZ(Plugin):
    def gen_message(self, parameter = None):
        try:
            driver = webdriver.PhantomJS() # or add to your PATH
            driver.set_window_size(1024, 768) # optional
            driver.get('http://www.metservice.com/towns-cities/wellington/wellington-city')
            section = driver.find_element_by_css_selector("#day6to10-disclaimer")
            l =  section.location

            r = [(int)(l['x']), int(l['y']), 650, 1250]
            url = self.filename_generator("jpg")
            driver.save_screenshot(url) # save a screenshot to disk
            im = Image.open(url)
            region = im.crop(r)
            region.save(url)
            return {"msg":"Weather Forecast", "pic":url}
        except:
            traceback.print_exc()
            return None

# WeatherNZ().gen_message()