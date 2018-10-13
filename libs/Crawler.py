
from .logger import logger
from .filters.FilterHandler import FilterHandler
from .aggregation.AgreggationHandler import AgreggationHandler
from .sources.SourceFile import SourceFile


class Crawler(object):

    def __init__(self, args):

        args = vars(args)

        self.rule = FilterHandler(args)
        self.aggregation = AgreggationHandler(args)
        self.source = SourceFile(args.get('src'))


    def run(self):

        with self.source.load() as file:
            for line in file:
                if self.rule.match(line):
                    self.result(line)

        if self.aggregation.activated():
            self.aggregation.out()

    def result(self, line):

        if self.aggregation.activated():
            self.aggregation.append(line)
            return

        logger.info(line)
