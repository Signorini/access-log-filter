
import re
import ipaddress
from libs.logger import logger


class RuleIP(object):

    def __init__(self, ip):

        self._reg = r'[0-9]+(?:\.[0-9]+){3}'

        try:
            self.network = ipaddress.ip_network(ip)
        except ValueError:
            logger.error("Not valid CIDR range - [%s]", ip)
            exit(1)


    def valid_ip(self, ip):
        try :
            return ipaddress.ip_address(ip)
        except ValueError:
            pass


    def check(self, ip):
        valid = self.valid_ip(ip)
        return valid and valid in self.network


    def match(self, str):
        ips = re.search(self._reg, str)

        if ips:
            ip = ips.group(0)
            if self.check(ip):
                return ip

    def match_all(self, str):
        ips = re.findall(self._reg, str)

        if ips:
            for ip in ips:
                if self.check(ip):
                    return ip