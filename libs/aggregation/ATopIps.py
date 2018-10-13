
import re
from collections import Counter
from .IAggregation import IAgreggation

class ATopIps(IAgreggation):

    def __init__(self, qtd):
        self._qtd = qtd
        super().__init__()


    def extract(self, str):
        ips = re.match( r'^[0-9]+(?:\.[0-9]+){3}', str)

        if ips:
            return ips.group(0)

    def ordered_result(self):
        cc = Counter(self._counter)
        return cc.most_common(self._qtd)

    def output(self):
        result = self.ordered_result()

        for item in result:
            line = 'RC (%s) [%s]' % (item[1], item[0])
            self.view(line)