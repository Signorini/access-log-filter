
from .logger import logger
from .filters.FilterHandler import FilterHandler
from .aggregation.AgreggationHandler import AgreggationHandler
from .sources.SourceFile import SourceFile

"""
Main class crawler, have three dependecy injection

-> FilterHandler: Handle with all filters
-> AggregationHandle: Handle all aggregation
-> SourceFile: Abstract interface for file system, can be extend for outher sources like dbs, streams and ext.

"""
class Crawler(object):

    def __init__(self, args):

        args = vars(args)

        self.rule = FilterHandler(args)
        self.aggregation = AgreggationHandler(args)
        self.source = SourceFile(args.get('src'))


    def run(self):
        """
        Loop Source File getting pointer resource,

        If have only filter commands each line will be print accordly each interation,
        if is aggreation command each line will be appended on the bag and print only on the end.
        """

        with self.source.load() as file:
            for line in file:
                if self.rule.match(line): #If have filter apply
                    self.result(line)

        if self.aggregation.activated(): #If have a aggregation command show the result
            self.aggregation.out()

    def result(self, line):

        if self.aggregation.activated(): #If have a aggregation command append on the bag
            self.aggregation.append(line)
            return

        logger.info(line)
