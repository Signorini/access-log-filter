
import re
import ipaddress
from libs.logger import logger


class RuleIP(object):
    """
        Filter by IP
    """

    def __init__(self, ip):
        """
            Check if cli arg ip it's valid

            Args:
                ip (:str/<IPv4>):
                    IPv4
        """
        try:
            self.network = ipaddress.ip_network(ip)  #standard pythno, network address or cidr
        except ValueError:
            logger.error("Not valid CIDR range - [%s]", ip)
            exit(1)


    def match(self, str):
        """
            Apply ip filter
            - Single regex to extract the first ip address
            - Check if its a real ip address
            - Compare if this ip is in the network

            Args:
                str (:str):
                    Single line
        """
        ips = re.search(r'[0-9]+(?:\.[0-9]+){3}', str)  #parse using regex, get the first ip address

        if ips:
            ip = ips.group(0)
            if self.check(ip):  #check ip this ip are on network. (network its created using a construct cli arg)
                return ip

    def valid_ip(self, ip):
        try :
            return ipaddress.ip_address(ip)
        except ValueError:
            pass


    def check(self, ip):
        valid = self.valid_ip(ip)  #check if its a real ip 0.0.0.0 to 255.255.255.255
        return valid and valid in self.network  #network its a list of all ip cidr range