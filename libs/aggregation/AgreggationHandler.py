
from .ATopIps import ATopIps
from .ARequests import ARequests
from .ATopSources import ATopSources


class AgreggationHandler(object):

    def __init__(self, args):
        """
            Orchestrator class, get all args, compare if exist any aggregation tag and set the right class

            To add more aggregator, create a class using IAgregation abstract class and register on mapp variable.

            Design Pattern - Chain of Responsability

            Args:
                args (:obj):
                    List with all cli args
        """

        self._mapp = {
            'top_ips': ATopIps,
            'request_rate': ARequests,
            'top_sources': ATopSources
        }

        self.active = False
        self.ag = self.setup(args)


    def setup(self, args):
        """
            Find which aggregator will be use, accordly cli args

            Args:
                args (:obj):
                    List with all cli args
        """
        for key, ags in self._mapp.items():
            arg = args.get(key)

            if arg:  #if exist, turn aggregator actived and create a new instance a new aggregator class
                self.active = True
                return ags(arg)


    def activated(self):
        return self.active

    def append(self, line):
        """
            Used by Crawler class, append a line on instance of aggregator setuped.

            Args:
                args (:str):
                    Single line inserted by Crawler loop
        """
        self.ag.append(line)

    def out(self):
        """
            Return the result accordly each aggregator
        """
        return self.ag.output()