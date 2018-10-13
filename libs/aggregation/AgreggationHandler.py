
from .ATopIps import ATopIps
from .ARequests import ARequests
from .ATopSources import ATopSources


class AgreggationHandler(object):

    def __init__(self, args):

        self._mapp = {
            'top_ips': ATopIps,
            'request_rate': ARequests,
            'top_sources': ATopSources
        }

        self.active = False
        self.ag = self.setup(args)


    def setup(self, dargs):

        for key, ags in self._mapp.items():
            arg = dargs.get(key)

            if arg:
                self.active = True
                return ags(arg)


    def activated(self):
        return self.active

    def append(self, line):
        self.ag.append(line)

    def out(self):
        return self.ag.output()