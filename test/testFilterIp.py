
import unittest

from libs.filters.rules.Ip import RuleIP


class RuleIPTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.ips = {
            'valid_ip': '78.29.246.2',
            'invalid_ip': '78.1231231.246.1455',
            'valid_cidr': '78.29.0.0/16',
            'invalid_cidr': '78.29.246.2/16'
        }

        self.strings = [
            "78.29.246.2 - - [02/Jun/2015:17:22:13 -0700] GET /E\?G=H6lijmCkc3hGIT",
            "78.29.246.20 - - Trick, 78.123.12312312.2, trick trick 34.45.12.12",
            "Trick, 78.123.12312312.2, without a valid ip"
        ]

    # executed after each test
    def tearDown(self):
        pass

    def test_valid_ip(self):
        valid = RuleIP(self.ips['valid_ip'])
        self.assertTrue(type(valid) is RuleIP)

    def test_invalid_ip(self):
        with self.assertRaises(SystemExit) as cm:
            RuleIP(self.ips['invalid_ip'])

        self.assertEqual(cm.exception.code, 1)

    def test_valid_cidr(self):
        valid = RuleIP(self.ips['valid_cidr'])
        self.assertTrue(type(valid) is RuleIP)

    def test_invalid_cidr(self):
        with self.assertRaises(SystemExit) as cm:
            RuleIP(self.ips['invalid_cidr'])

        self.assertEqual(cm.exception.code, 1)

    def test_valid_ip_match(self):
        filter = RuleIP(self.ips['valid_ip'])

        valid = []

        for line in self.strings:
            vv = filter.match(line)

            if vv:
                valid.append(vv)

        self.assertEqual(len(valid), 1)
        self.assertEqual(valid[0], self.ips['valid_ip'])


    def test_valid_cidr_match(self):
        filter = RuleIP(self.ips['valid_cidr'])

        valid = []

        for line in self.strings:
            vv = filter.match(line)
            if vv:
                valid.append(vv)

        self.assertEqual(len(valid), 2)
        self.assertEqual(valid[0], self.ips['valid_ip'])

if __name__ == "__main__":
    unittest.main()