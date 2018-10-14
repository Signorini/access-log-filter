
import re
from functools import reduce
from .IAggregation import IAgreggation

class ARequests(IAgreggation):

    def __init__(self, args):
        mapp = {
            'hour': 2,
            'minutes': 3
        }

        self._hist = mapp.get(args, 3)
        super().__init__()


    def extract(self, str):
        """
            Extract time and create hash

            Ex:
            168.235.196.131 [24/Oct/2016:00:02:40 -0700] 0.000 https .com "GET /staticx/udemy/css/fancybox_overlay.png HTTP/1.1" 404 162

            Will extract 24/Oct/2016:00:02:40,
            with this value split : and slice accordly arg (minute = 3 or hour = 2)
            apply reduce function to create hash like 24/Oct/20160002 for minutes or 24/Oct/201600 for hour

            Args:
                str (:str):
                    Single line
        """
        time = re.search(r'[0-9]{2}/[A-Za-z]+/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}', str)

        if time:
            tt = time.group().split(':')  #['24/Oct/2016', '00', '02', '40']
            stime = tt[0:self._hist]  # minutes 2 -> ['24/Oct/2016', '00', '02']
            tmp = reduce(lambda a, b: a + b, stime)  #reduce 24/Oct/20160002 this is my hash
            return tmp

    def ordered_result(self):
        return self._counter

    def output(self):
        """
            Split hash and create log line
        """
        for key, item in self.ordered_result().items():
            line = '%s - [%s:%s] | RC %s' % (key[0:11], key[11:13], key[13:15], item)
            self.view(line)
