from .Time import RuleTime


class RuleEnd(RuleTime):

    def __init__(self, time):
        super().__init__(time, "lower")