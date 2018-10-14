
## Script - Analyses access logs IP - (Access logs)

Analyses access logs (apache or nginx), can filters by ip, start and end time, aggregate information by top ips, request rate or top whois access ip, used to finding malicious tried access, fast analyses, networks flows, hot links and more.

### Usage:
```bash
python3 cli.py --ip 10.10.10.10 --src ./my-access-logs.txt
#with cidr 
python3 cli.py --ip 10.10.0.0/16 --src ./my-access-logs.txt
#help
python3 cli.py --help

bash
weblog.sh --ip 10.10.0.0/16 --src ./my-access-logs.txt
```

Wil return:
```bash
10.10.10.10 - - [02/Jun/2015:17:21:57 -0700] "GET /logs/access.log HTTP/1.1" 200 54049 "http://prograf1mgwuf.forumcircle.com" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36" "redlug.com"
10.10.23.07 - - [02/Jun/2015:17:21:58 -0700] "GET /J?l=71AwNIQ1Bxdsaaqq HTTP/1.1" 404 73 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"
10.10.23.10 - - [02/Jun/2015:17:21:59 -0700] "GET /zKnjR7uvIsgmyYeEG8jl1T/Odzg HTTP/1.1" 404 73 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"
```

#### Filter - Ip:

Output log lines which matches either the < IP address > or the < IP range CIDR >.

```bash
python3 cli.py --ip 10.10.10.10 --src ./my-access-logs.txt
#with cidr 
python3 cli.py --ip 10.10.0.0/16 --src ./my-access-logs.txt
```


#### Filter - Start and End (HH:MM):

Only process lines after/before the given time

```bash
python3 cli.py --start 19:00 --src ./log_test_acess.txt
#with cidr 
python3 cli.py --start 19:00 --end 22:00 --src ./log_test_acess.txt
```

PS: Allowed only HH:MM format.


#### Aggregation - Top Ips < Number >:

The top <Number> of IP addresses by request count.

Default: 50

```bash
python3 cli.py --top-ips 10 --src ./log_test_acess.txt
```

```bash
RC (4) [218.183.138.183]
RC (2) [218.210.124.144]
RC (1) [218.28.72.18]
RC (1) [218.234.33.60]
```


#### Aggregation - Top Ips Source < Number >:

Lists the top <Number> IP owners based on the whois information. Information about WHOIS:

Default: 5

```bash
python3 cli.py --top-sources 10 --src ./log_test_acess.txt
```

```bash
[218.183.138.183](4) -> | asn: 17676 | asn_country_code: JP | asn_date: 2001-10-10 | asn_description: GIGAINFRA Softbank BB Corp., JP | asn_registry: apnic | entities: ['IRT-SOFTBANK-JP', 'SA421-AP']
[218.210.124.144](2) -> | asn: 9919 | asn_country_code: TW | asn_date: 2005-07-07 | asn_description: NCIC-TW New Century InfoComm Tech Co., Ltd., TW | asn_registry: apnic | entities: []
[218.28.72.18](1) -> | asn: 4837 | asn_country_code: CN | asn_date: 2001-04-12 | asn_description: CHINA169-BACKBONE CHINA UNICOM China169 Backbone, CN | asn_registry: apnic | entities: ['CH1302-AP', 'WW444-AP', 'IRT-CU-CN']
[218.234.33.60](1) -> | asn: 9318 | asn_country_code: KR | asn_date: 2002-04-30 | asn_description: SKB-AS SK Broadband Co Ltd, KR | asn_registry: apnic | entities: ['IM670-AP', 'IRT-KRNIC-KR']
```

#### Aggregation - Request Rate < hour | minutes >:

Prints out the request count per minute or hour.

Default: minutes

```bash
python3 cli.py --request-rate --src ./log_test_acess.txt
#or
python3 cli.py --request-rate hour --src ./log_test_acess.txt
```

```bash
24/Oct/2016 - [17:05] | RC 1
24/Oct/2016 - [17:10] | RC 1
24/Oct/2016 - [17:36] | RC 2
24/Oct/2016 - [17:51] | RC 1
24/Oct/2016 - [17:57] | RC 1
24/Oct/2016 - [18:02] | RC 1
24/Oct/2016 - [21:15] | RC 1
```

#### Chaining args:

You can chaining all filters and used with aggregation, but only one aggregation can be use in the same time.

```bash
python3 cli.py --ip 218.0.0.0/8 --start 17:00 --top-source 5 --src logs/log_test_acess.txt
```

Only will show 5 top source filtered by 218./8 ips and after 17:00

-------

### Setup and installation (Develop)

##### Requiriments
* Python >3.5
    * ipaddress (>3.3)
    * asyncio (>3.5)
    
    * Embedded dnspython
    * Embedded ipwhois (with changes to be compatible with python 3.5)


##### Development

The assumption you already have python 3 and virtualev installed

Initialize and active virtual env

Executing

```bash
virtualenv -p python3 .
source bin/activate
```

##### Test

Minimal Testing code

- Integration test code
    - FilterIp
    - FilterStart
    - FilterEnd
    - Aggregation Top IPs
    - Aggregation Request rate

```bash
python3 -m unittest discover
```

##### Folder structure

- **libs**
    - **aggregation**: All aggregation domain
        - AgreggationHandler.py: Aggregate Orchestrator (Chain of responsability pattern)
        - IAggregation.py: Abstract Class - Aggregation Contract
        - ARequests.py / ATopIps.py / ATopSources.py: Concrete aggregator (Strategy pattern)
        
    - **filters**: All rules filters
        - **rules**: Filter rules (Decorator pattern)
            - Time.py: Time filter
            - Start.py / End.py: Extend time filter class. (Open/close solid)
            - Ip.py: Ip rules
        - FilterHandler.py: Filter Orchestrator (Chain of responsability pattern)
        
    - **sources**: Source repositories class
        - SourceFile.py: Read file system

- **logs**: Static logs files
- **vendor**: 3 party libraries
    - **dns**: http://www.dnspython.org/
    - **ipwhois**: https://pypi.org/project/ipwhois/
    
- **test**: Minimal test, ensure filters and aggregations are working.

##### Computer Science metrics and scaling points

Assumptions Points

- Complexity Time
    - Ip filter and time **O(n)**
    - Tops Ips and Request Rate **O(n)**
    - Top Source **O(n + y)** (n log size and y qtd top ip)
    
- Complexity Space
    - Ip filter and time **O(n)**
    - Tops Ips and Request Rate **O(n)**
    - Top Source **O(n + 2y)** (Don't have any recursive situation, 
    but the script use 2y data structure to be performatic) (n log size, y qtd top show)
    
- Using "with" statement, internally python will control a streaming on file line by line, 
**won't have a memory problem**.
 
- Whois issue
    - The top-source it's a heavy tasks, each IP need to be requested to whois rdap servers
        - Can create cache system on redis or using pickle file, each request its cached with TTL flag, 
    reducing a quantity of request and mitigating RDAP rate limit struggles.
        - We use event loop strategy to parallelism task (asyncio), i/o bound problem, we can use system cache 
        together with task event to syncronize and control whois data.
    
- Start and End, extend to month and days
- Time filters only comparer hour and minutes, for a month need to create a class map, how is in charge of translate string month in number (oct -> 10)

###### Production env

If need a robust log analyser, we recommend to use ELK or graylog stack, have a power of centralized log system, 
with search enginner to aggregate and metrify logs.