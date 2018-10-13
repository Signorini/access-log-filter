
import re
import time
import datetime
from libs.logger import logger


class RuleTime(object):

    def __init__(self, time, cmp):
        time = re.match(r'^[0-9]{2}:[0-9]{2}$', time)

        if time:
            self.timer = self.ddtime(time)
            self.cmp = cmp

        else:
            logger.error("Invalid time format <HH:MM> - [%s]", time)
            exit(1)


    def ddtime(self, time):
        strtime = time.group(0).replace(":", "")
        return int(strtime)

    def match(self, str):
        time = re.search(r'[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}', str)

        if time:
            tt = time.group().split(':')

            strtime = tt[1] + tt[2]
            itime = int(strtime)

            return self.statement(itime, self.timer)


    def statement(self, first, second):

        if self.cmp is 'greater':
            return first >= second

        if self.cmp is 'lower':
            return first <= second