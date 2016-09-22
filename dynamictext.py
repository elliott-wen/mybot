# -*- coding: utf-8 -*-
from plugin import Plugin
import traceback
import random
from PIL import Image, ImageDraw, ImageFont
import imgs2gif

class DynamicText(Plugin):

    def gen_message(self, parameter = None):
        try:
            if parameter == None:
                return None
            windows_size = 500
            windows_forward = 80
            strs = "   ".join(parameter)
            FONT_PATH = "font.ttf"
            font = ImageFont.truetype(FONT_PATH, 80)
            font_width, font_height = font.getsize(strs)
            canvas_width = (int)(font_width*3.1)
            canvas_height = font_height*2
            img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255)) # 创建图形
            draw = ImageDraw.Draw(img) # 创建画笔
            draw.text((canvas_height/3, canvas_height/4), strs, font=font, fill=(random.randint(0,30), random.randint(0,30), random.randint(0,30)))
            current_pos = 0
            imgs = []
            if windows_size > canvas_width:
                imgs.append(img)
            else:
                while current_pos + windows_size < canvas_width:
                    imgs.append(img.crop([current_pos, 0 ,current_pos+windows_size, font_height*2]))
                    current_pos += windows_forward
            filegif = self.filename_generator("gif")
            imgs2gif.writeGif(filegif, imgs, duration=0.1)
            return {"pic":filegif}
        except:
            traceback.print_exc()
            return None

