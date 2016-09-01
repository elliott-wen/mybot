import string
import random
import os
import time
class Plugin(object):
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'data');
        self.quota = 0
        self.quota_time = time.time()


    def filename_generator(self, postfix, size=9, chars=string.ascii_uppercase + string.digits):
        randomString = ''.join(random.choice(chars) for _ in range(size))
        return os.path.join(self.data_path, randomString + "." +postfix)

    def gen_message(self, caller_id = None, message = None):
        return None

    def quota_check(self):
        if time.time() > self.quota_time + 60:
            self.quota_time = time.time()
            self.quota = 0

        self.quota += 1
        if self.quota < 30:
            return True
        else:
            return False

