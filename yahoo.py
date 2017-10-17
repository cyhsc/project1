import os
import sys
import time
from urllib2 import urlopen
import utils
import config

class Yahoo:

    def __init__(self):
        pass

    def basic(self, sym):

        url = 'http://download.finance.yahoo.com/d/quotes.csv?s=' + sym + '&f=d1ohgl1vc1p2a2'
        print url
        html_doc = urlopen(url).read()
        lines = html_doc.split('\n')
        items = lines[0].split(',')
        
        res = {}
        res['date'] = items[0].strip('"')
        res['open'] = items[1]
        res['high'] = items[2]
        res['low'] = items[3]
        res['close'] = items[4]
        res['volume'] = items[5]
        res['change'] = items[6]
        res['percent_change'] = items[7].strip('"')
        res['average_volume'] = items[8]
        
        return res
