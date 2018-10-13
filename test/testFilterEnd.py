import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + '/vendor')

import unittest

from libs.filters.rules.End import RuleEnd


class RuleEndTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.filter = {
            'valid': '19:00',
            'invalid': '123:23'
        }

        self.strings = [
            "78.29.246.2 - - [02/Jun/2015:17:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.2 - - [02/Jun/2015:18:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.2 - - [04/Jun/2015:19:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.2 - - [05/Jun/2015:20:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.2 - - [06/Jun/2015:21:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
        ]

    # executed after each test
    def tearDown(self):
        pass

    def valid_entry(self):
        valid = RuleEnd(self.filter['valid'])
        self.assertTrue(type(valid) is RuleEnd)

    def test_invalid_entry(self):
        with self.assertRaises(SystemExit) as cm:
            RuleEnd(self.filter['invalid'])

        self.assertEqual(cm.exception.code, 1)

    def test_valid_time_match(self):
        filter = RuleEnd(self.filter['valid'])

        valid = []

        for line in self.strings:
            vv = filter.match(line)

            if vv:
                valid.append(line)

        self.assertEqual(len(valid), 2)
        self.assertEqual(valid[0], self.strings[0])
        self.assertEqual(valid[1], self.strings[1])

if __name__ == "__main__":
    unittest.main()