
from collections import Counter
from functools import reduce
from ipwhois import IPWhois
from .ATopIps import ATopIps


class ATopSources(ATopIps):

    def parseWhoisRDAP(self, ip):
        obj = IPWhois(ip)
        whois = obj.lookup_rdap(inc_nir=False, inc_raw=False)

        return {k: whois.get(k, None) for k in
                 ('asn', 'asn_country_code', 'asn_date', 'asn_description', 'asn_registry', 'entities')}

    def output(self):
        result = self.ordered_result()

        for item in result:
            data = self.parseWhoisRDAP(item[0])
            asn = reduce(lambda x, key: '%s | %s: %s' % (x, key, data[key]), data, '')
            line = '[%s](%s) -> %s' % (item[0], item[1], asn)
            self.view(line)