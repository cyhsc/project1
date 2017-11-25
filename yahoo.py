import os
import sys
import time
import urllib2
from urllib2 import urlopen
import utils
import config

class Yahoo:

    def __init__(self):
        pass

    def basic(self, sym):

        url = 'http://download.finance.yahoo.com/d/quotes.csv?s=' + sym + '&f=d1ohgl1vc1p2a2j1d1m3m4'
        print url

        req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })

        #html_doc = urlopen(url).read()
        html_doc = urlopen(req).read()
        lines = html_doc.split('\n')
        items = lines[0].split(',')

        res = {}

        for item in items: 
            if item == 'N/A':
                return None

        res['date'] = items[0].strip('"')
        res['open'] = items[1]
        res['high'] = items[2]
        res['low'] = items[3]
        res['close'] = items[4]
        res['volume'] = items[5]
        res['change'] = items[6]
        res['percent_change'] = items[7].strip('"')
        res['average_volume'] = items[8]
        res['capitalization'] = items[9]
        date = items[10].strip('"')
        print date
        date = date.split('/')
        print date
        date_str = date[2] + '-' + date[0] + '-' + date[1]
        res['last_trading_date'] = date_str
        res['ma50'] = items[11]
        res['ma200'] = items[12]
        
        return res
