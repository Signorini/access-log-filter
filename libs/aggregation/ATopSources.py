
import asyncio
import concurrent.futures
from functools import reduce

from vendor.ipwhois import IPWhois
from .ATopIps import ATopIps
from ..logger import logger


class ATopSources(ATopIps):
    """
        Extend ATopIps aggregation,
        -> get top ip result,
        -> after find whois information using RDAP request, doing using parallelism tasks
        -> merge the result and ordered
    """

    def __init__(self, qtd):
        self._tmp = {}
        super().__init__(qtd)

    def output(self):
        """
            Initialize Event Loop using asyncio lib
            RDAP request it's a blocking standard python library, need to create a executor to handle it with threads
            Run until all task it' done
            Close the loop
        """

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        loop.run_until_complete(self.mfuture(loop, executor))  # call coroutine method self.mfuture
        loop.close()

    async def mfuture(self, loop, executor):
        """
            Create task list and run, using event loop with coroutines

            1 - Get a Top Ips result using parent class method (top ips ordered_result())
            2 - Append tasks, each task it's asyncio executor
            3 - Gather and await to finish all tasks
            4 - Re order the result
        """
        result = self.ordered_result()

        task_list = []
        for item in result:
            task_list.append(loop.run_in_executor(executor, self.get_whois, item[0]))

        await asyncio.gather(*task_list)
        self.ordered_out()

    def ordered_out(self):
        result = self.ordered_result() #retrive ordered result, iterate and use hashtable tmp to add whois information

        logger.info("[Info] Ordering...")
        for item in result:
            data = self._tmp[item[0]]
            asn = reduce(lambda x, key: '%s | %s: %s' % (x, key, data[key]), data, '')
            line = '[%s](%s) ->%s' % (item[0], item[1], asn)
            self.view(line)

    def get_whois(self, ip):
        """
            Single task, request the rdap info, and put on shared variable, using hash to control race conditions.

            -> get top ip result,
            -> after find whois information using RDAP request, doing using parallelism tasks
            -> merge the result and ordered
        """
        res = self.parse_whois_RDAP(ip)  # RDAP Request
        self._tmp[ip] = res  # Put the data on shared class variable
        logger.info("[Info] Process %s" % ip)

    def parse_whois_RDAP(self, ip):
        obj = IPWhois(ip)  # 3 party library, use dns python and rdap endpoints
        whois = obj.lookup_rdap(inc_nir=False, inc_raw=False, rate_limit_timeout=60, retry_count=2)

        return {k: whois.get(k, None) for k in
                ('asn', 'asn_country_code', 'asn_date', 'asn_description', 'asn_registry', 'entities')}