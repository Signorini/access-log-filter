import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + '/vendor')

import unittest

from libs.aggregation.ATopIps import ATopIps


class ATopIpsTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.results = [('78.29.246.2', 3), ('78.29.246.20', 2), ('66.249.75.128', 1)]

        self.strings = [
            "78.29.246.2 - - [02/Jun/2015:17:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.20 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "78.29.246.2 - - [02/Jun/2015:19:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.20 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "78.29.246.2 - - [02/Jun/2015:20:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "66.249.75.128 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "Trick, 78.123.12312312.2, without a valid ip"
        ]

    # executed after each test
    def tearDown(self):
        pass

    def test_aggregation(self):
        aggregator = ATopIps(3)

        for line in self.strings:
            aggregator.append(line)

        data = aggregator.ordered_result()

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], self.results[0])
        self.assertEqual(data[1], self.results[1])
        self.assertEqual(data[2], self.results[2])


if __name__ == "__main__":
    unittest.main()