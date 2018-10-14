
from .rules.Ip import RuleIP
from .rules.Start import RuleStart
from .rules.End import RuleEnd


class FilterHandler(object):

    def __init__(self, args):
        """
            Orchestrator class, get all args, compare if exist any filter tag and set the right class
            Filter can be chain, put all class on self.filters list

            To create a new filter, create a class and register on mapp var. (cli arg -> class used)

            Design Pattern - Chain of Responsability and Strategy

            Args:
                args (:obj):
                    List with all cli args
        """

        self._mapp = {
            'ip': RuleIP,
            'start': RuleStart,
            'end': RuleEnd
        }

        self.filters = []
        self.setup(args)


    def setup(self, dargs):
        """
            Find which filter will be use, accordly cli args

            Args:
                args (:obj):
                    List with all cli args
        """
        for key, filter in self._mapp.items():

            arg = dargs.get(key)
            if arg:
                self.filters.append(filter(arg))  #Create new instance and append into var - RuleClass(<cli arg>)


    def match(self, line):
        """
            Check if this line match with any instance filter.

            Args:
                line (:str):
                    Single line
        """
        for check in self.filters:  #iterate all instance filter
            r = check.match(line)   #check if pass
            if not bool(r):
               return False         #if not return false, Crawler class will ignore this line

        return True                 #if yes, Crawler class will show the line or append on the bag (aggregation process)
