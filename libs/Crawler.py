
from .logger import logger
from .filters.FilterHandler import FilterHandler
from .aggregation.AgreggationHandler import AgreggationHandler
from .sources.SourceFile import SourceFile

"""
Main class crawler, responsible for orchestrating and run the app, separate for three steps

1 - Use SourceHandle to open and read source data, can be a file, db or anything
2 - Iterate each line provide by Source and pass to a list of filters, this filters it's activated by cli arg
3 - Exit two types of result, a single line result or an aggregation result
	- Single line results it's only a logs file filters, normally the output its made on the line
	- Aggregation results, it's an aggregate data result, its process by class and the output its made only in the end.

Dependency Injection
-> FilterHandler: Handle with all filters
-> AggregationHandle: Handle all aggregation
-> SourceFile:  Abstract interface for file system, can be extended for other sources like dbs, streams and ext.

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

        Info
        - Complexity Time
            - Ip filter and time O(n)
            - Tops Ips and Request Rate O(n)
            - Top Source O(n + y) (n log size and y qtd top ip)

        - Complexity Space
            - Ip filter and time O(1)
            - Tops Ips and Request Rate O(y)
            - Top Source O(2y) (Don't have any recursive situation,
            but the script use 2y data structure to be performatic) (n log size, y qtd top show)
        """

        with self.source.load() as file:
            for line in file:
                if self.rule.match(line):  #If have filter apply
                    self.result(line)

        if self.aggregation.activated():  #If have any aggregation command, show the result
            self.aggregation.out()

    def result(self, line):

        if self.aggregation.activated():  #If have any aggregation command, append the line on the bag
            self.aggregation.append(line)
            return

        logger.info(line)
