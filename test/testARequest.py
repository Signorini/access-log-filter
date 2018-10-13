import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + '/vendor')

import unittest

from libs.aggregation.ARequests import ARequests


class ARequestTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.results = {'02/Jun/20151722': 2, '02/Jun/20152022': 1}


        self.strings = [
            "78.29.246.2 - - [02/Jun/2015:17:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.20 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "78.29.246.2 - - [02/Jun/2015:17:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.20 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "78.29.246.2 - - [02/Jun/2015:20:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "66.249.75.128 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "Trick, 78.123.12312312.2, without a valid ip"
        ]

    # executed after each test
    def tearDown(self):
        pass

    def test_aggregation(self):
        aggregator = ARequests(3)

        for line in self.strings:
            aggregator.append(line)

        data = aggregator.ordered_result()

        self.assertEqual(len(data), 2)
        self.assertEqual(data['02/Jun/20151722'], self.results['02/Jun/20151722'])
        self.assertEqual(data['02/Jun/20152022'], self.results['02/Jun/20152022'])


if __name__ == "__main__":
    unittest.main()