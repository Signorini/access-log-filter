
from ..logger import logger

class IAgreggation(object):
    """
        Abstract class - IAggregation, used to create a aggregation rule.

        Design Pattern - Decorator
    """

    def __init__(self):
        self._counter = {}  #initialize a counter var

    # contracts methods
    #
    # I know, regarding OO principles, contract methods its define only on interfaces,
    # abstract class have some bases implementation
    # and concrete class its a full customize implementation.

    def extract(self):
        pass

    def ordered_result(self):
        pass

    def append(self, str):
        data = self.extract(str)  #call implemented extract method
        if data:
            self.increase_count(data)  #call implemented increase count method

    def increase_count(self, hash):
        """
            Algorithm - HashTable T O(1) - S O(n)

            Increment 1 to specific hash

            Args:
                hash (:str):
                    Agreggate hash, can be a ip or time
        """

        if hash in self._counter:
            self._counter[hash] += 1
        else:
            self._counter[hash] = 1

    def view(self, line):
        """
            Show the result
            -> Can create a robust view class, to send the result to a file, DB or any necessary receiver
        """
        logger.info(line)

    def output(self):
        pass