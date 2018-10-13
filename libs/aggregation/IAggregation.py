
from ..logger import logger

class IAgreggation(object):

    def __init__(self):
        self._counter = {}

    def append(self, str):
        data = self.extract(str)
        if data:
            self.increase_count(data)

    def increase_count(self, hash):
        if hash in self._counter:
            self._counter[hash] += 1
        else:
            self._counter[hash] = 1

    def view(self, line):
        logger.info(line)

    def output(self):
        pass