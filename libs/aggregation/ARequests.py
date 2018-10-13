
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
        time = re.search(r'[0-9]{2}/[A-Za-z]+/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}', str)

        if time:
            tt = time.group().split(':')
            stime = tt[0:self._hist]
            tmp = reduce(lambda a, b: a + b, stime)
            return tmp

    def output(self):

        for key, item in self._counter.items():
            line = '%s - [%s:%s] | RC %s' % (key[0:11], key[11:13], key[13:15], item)
            self.view(line)
