
from .rules.Ip import RuleIP
from .rules.Start import RuleStart
from .rules.End import RuleEnd


class FilterHandler(object):

    def __init__(self, args):

        self._mapp = {
            'ip': RuleIP,
            'start': RuleStart,
            'end': RuleEnd
        }

        self.filters = []
        self.setup(args)


    def setup(self, dargs):

        for key, filter in self._mapp.items():

            arg = dargs.get(key)
            if arg:
                self.filters.append(filter(arg))


    def match(self, line):

        for check in self.filters:
            r = check.match(line)
            if not bool(r):
               return False

        return True
