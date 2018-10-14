
import re
import time
import datetime
from libs.logger import logger


class RuleTime(object):

    def __init__(self, time, cmp):
        """
            Check if cli arg start or/and end it's valid time (Its not deep real valid time, but for performance, execute only one regex).

            Args:
                time (:str/<HH:MM>):
                    Time in hour and minutes
                cmp (:str)
                    Greater or lower than
        """
        time = re.match(r'^[0-9]{2}:[0-9]{2}$', time)

        if time:
            self.timer = self.ddtime(time)
            self.cmp = cmp

        else:
            logger.error("Invalid time format <HH:MM> - [%s]", time)
            exit(1)


    def match(self, str):
        """
            Extract time

            Ex line:
            168.235.196.131 [24/Oct/2016:00:02:40 -0700] 0.000 https .com "GET /staticx/udemy/css/fancybox_overlay.png HTTP/1.1" 404 162

            Will extract 24/Oct/2016:00:02:40,
            Get hour and minute and concatenate (02:40 -> 0240)
            Typecast to int
            Do conditional using self.cmp statement

            Args:
                str (:str):
                    Single line
        """
        time = re.search(r'[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}', str)

        if time:
            tt = time.group().split(':')

            strtime = tt[1] + tt[2]
            itime = int(strtime)

            return self.statement(itime, self.timer)  #conditional using two number (02:40 > 01:34 -> 240 > 134)

    def ddtime(self, time):
        strtime = time.group(0).replace(":", "")  #Get hour and minute and concatenate (02:40 -> 0240)
        return int(strtime)

    def statement(self, first, second):

        if self.cmp is 'greater':
            return first >= second

        if self.cmp is 'lower':
            return first <= second