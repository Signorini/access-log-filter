from distutils.core import setup

setup(
    name = 'Ip Finder',
    version = '0.1.0',
    description = '<IP Finder> - Find all lines in files logs with specific ip or cidr range.',
    author = 'Felipe Signorini',
    author_email = 'felipeklerk@yahoo.com.br',
    url = 'https://github.com/Signorini/ip-finder',
    py_modules=['iplog'],
    install_requires=[
        "ipaddress==1.0.22"
    ],
    entry_points='''
        [console_scripts]
        iplog=cli
    '''
)