
import re
from collections import Counter
from .IAggregation import IAgreggation

class ATopIps(IAgreggation):

    def __init__(self, qtd):
        self._qtd = qtd
        super().__init__()


    def extract(self, str):
        """
            Extract first match ip, only for aggregation

            Ex:
            168.235.196.131 [24/Oct/2016:00:02:40 -0700] 0.000 https .com "GET /staticx/udemy/css/fancybox_overlay.png HTTP/1.1" 404 162

            Will extract 168.235.196.131,
            will be the hash value O(1)

            Args:
                str (:str):
        """

        ips = re.match( r'^[0-9]+(?:\.[0-9]+){3}', str)

        if ips:
            return ips.group(0)

    def ordered_result(self):
        """
            Use standard Counter class to order the top used ip
        """
        cc = Counter(self._counter)
        return cc.most_common(self._qtd)  #qtd is a cli arg used on --top-ips <number>

    def output(self):
        result = self.ordered_result()

        for item in result:
            line = 'RC (%s) [%s]' % (item[1], item[0])
            self.view(line)