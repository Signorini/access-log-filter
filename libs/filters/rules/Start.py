
from .Time import RuleTime


class RuleStart(RuleTime):

    def __init__(self, time):
        super().__init__(time, "greater")