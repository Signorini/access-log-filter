

## Script - Filter line by IP - (Access logs)

Find all lines in files logs with specific ip or cidr range, used for find malicious tried access, fast analyses and follow flows networks.

### Usage:
```bash
python cli.py --ip 10.10.10.10 --src ./my-access-logs.txt
with cidr 
python cli.py --ip 10.10.0.0/16 --src ./my-access-logs.txt

bash
weblog.sh --ip 10.10.0.0/16 --src ./my-access-logs.txt
```

Wil return:
```bash
10.10.10.10 - - [02/Jun/2015:17:21:57 -0700] "GET /logs/access.log HTTP/1.1" 200 54049 "http://prograf1mgwuf.forumcircle.com" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36" "redlug.com"
10.10.23.07 - - [02/Jun/2015:17:21:58 -0700] "GET /J?l=71AwNIQ1Bxdsaaqq HTTP/1.1" 404 73 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"
10.10.23.10 - - [02/Jun/2015:17:21:59 -0700] "GET /zKnjR7uvIsgmyYeEG8jl1T/Odzg HTTP/1.1" 404 73 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"
78.29
```


### Setup and installation (Develop)

##### Requiriments
* Python >3.5
    * ipaddress (>3.3)
    * asyncio (>3.5)


Executing

```bash
python cli.py --help

python cli.py --ip 157.55.39.109/32 --src logs/public_access.log.txt 
```

or using bash

```bash
chmod +x weblog.sh
./weblog.sh --ip 157.55.39.109/32 --src logs/public_access.log.txt
```

##### Test

Testing code

```bash
python -m unittest discover
```

##### Development

The assumption you already have python 3 and virtualev installed

Initialize and active virtual env

```bash
virtualenv -p python3 .
source bin/activate
```