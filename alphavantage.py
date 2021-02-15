import os
import sys
import time
from urllib2 import urlopen
import urllib2
import pandas as pd
import random
import utils
import config

class AV:

    def __init__(self, last_date = None):
	print("Hello world")
        self.key = config.get_alphavantage_key()
        self.last_date = last_date

    def form_dataframe(self, lines):
        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for line in lines:

            items = line.strip('\r\n').split(',')

            if self.last_date != None: 
                if items[0] > self.last_date:
                    break
                
            dates.append(items[0])
            open.append(float(items[1]))
            high.append(float(items[2]))
            low.append(float(items[3]))
            close.append(float(items[4]))
            volume.append(int(items[5]))

        df = pd.DataFrame(index = dates)
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume
        
        return df

    def get_quotes(self, url):
        try:
            print url
            results = urlopen(url)
            lines = results.readlines()[1:]
            lines = lines[::-1]
            return self.form_dataframe(lines[1:])

        except urllib2.URLError as e:
            print 'Failed to open', url, 'because of', e.reason
            return None
       
    def compact_quotes(self, sym):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
        url = url + '&symbol=' + sym + '&outputsize=compact&datatype=csv&apikey=' + self.key
        i = 0
        while True:
            df = self.get_quotes(url)    
            if df is not None:
                break
            i = i + 1
            n = random.randint(1, 10)
            print 'Retry #' + str(i) + ', Sleep for ' + str(n) + ' seconds ........'
            time.sleep(n)
        return df

    def full_quotes(self, sym):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
        url = url + '&symbol=' + sym + '&outputsize=full&datatype=csv&apikey=' + self.key
        i = 0
        while True:
            df = self.get_quotes(url)
            if df is not None:
                break
            i = i + 1
            n = random.randint(1, 10)
            print 'Retry #' + str(i) + ', Sleep for ' + str(n) + ' seconds ........'
            time.sleep(n)
        return df

def main(argv):

    av = AV()
    df = av.compact_quotes('SPY')
    print df
    av = AV('2017-11-27')
    df = av.compact_quotes('CSCO')
    print df

if __name__ == '__main__':
    main(sys.argv[1:])
