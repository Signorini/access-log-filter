import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + '/vendor')

import argparse
from libs.Crawler import Crawler


parser = argparse.ArgumentParser(description='<IP Finder> - Find all lines in files logs with specific ip or cidr range.')

parser.add_argument("--src", type=str,
                    default="./access.log.txt",
                    help='Source file path')

parser.add_argument("--ip", type=str,
                    help='Ip to find, can be absolute ip (10.10.128.100) or CIDR notation (10.10.0.0/16)')

parser.add_argument("--top-ips", type=int, const=50, nargs='?',
                    help='The top <Number> of IP addresses by request count.')

parser.add_argument("--request-rate", type=str, const='minute', nargs='?',
                    help='Prints out the request count per <metric> (Metric can be hour or minutes).')

parser.add_argument("--start", type=str,
                    help='Show only lines match after given time (HH:MM)')

parser.add_argument("--end", type=str,
                    help='Show only lines match before given time (HH:MM)')

parser.add_argument("--top-sources", type=int, const=5, nargs='?',
                    help='Lists the top <Number> IP owners based on the whois information')

if __name__ == "__main__":
    args = parser.parse_args()
    Crawler(args).run()