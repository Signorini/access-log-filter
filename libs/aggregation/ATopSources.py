
import asyncio
import concurrent.futures
from functools import reduce

from vendor.ipwhois import IPWhois
from .ATopIps import ATopIps
from ..logger import logger


class ATopSources(ATopIps):

    def __init__(self, qtd):
        self._tmp = {}
        super().__init__(qtd)

    def parse_whois_RDAP(self, ip):
        obj = IPWhois(ip)
        whois = obj.lookup_rdap(inc_nir=False, inc_raw=False, rate_limit_timeout=60, retry_count=2)

        return {k: whois.get(k, None) for k in
                ('asn', 'asn_country_code', 'asn_date', 'asn_description', 'asn_registry', 'entities')}

    def get_whois(self, ip):
        res = self.parse_whois_RDAP(ip)
        self._tmp[ip] = res
        logger.info("[Info] Process %s" % ip)

    async def mfuture(self, loop, executor):
        result = self.ordered_result()

        task_list = []
        for item in result:
            task_list.append(loop.run_in_executor(executor, self.get_whois, item[0]))

        await asyncio.gather(*task_list)
        self.ordered_out()

    def ordered_out(self):
        result = self.ordered_result()

        logger.info("[Info] Ordering...")
        for item in result:
            data = self._tmp[item[0]]
            asn = reduce(lambda x, key: '%s | %s: %s' % (x, key, data[key]), data, '')
            line = '[%s](%s) ->%s' % (item[0], item[1], asn)
            self.view(line)


    def output(self):
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        loop.run_until_complete(self.mfuture(loop, executor))
        loop.close()
