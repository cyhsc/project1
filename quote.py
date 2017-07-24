
#############################################################################
#  This uses quandl.com data. The format is 
#
#    Date,Open,High,Low,Close,Volume,Ex-Dividend,Split Ratio,Adj. Open,Adj. High,Adj. Low,Adj. Close,Adj. Volume
#############################################################################

from urllib2 import urlopen
from datetime import datetime
import pandas as pd
import json
import warnings
import config
import utils

warnings.simplefilter(action='ignore', category=FutureWarning)

CONFIG_DIR = config.CONFIG_DIR

DEFAULT_LOOKBACK = 3

class Quote:

    def __init__(self, fresh_data = False, lookback = DEFAULT_LOOKBACK):
        self.year, self.month, self.day, self.weekday = utils.date_and_time()
        self.lookback = lookback
        self.fresh_data = fresh_data
        self.quandl_key = open(CONFIG_DIR + 'quandl_key', 'r').readline().strip('\n')

    def form_url_quandl(self, sym):
        start = str(self.year - self.lookback) + '-' + str(self.month) + '-' + str(self.day)
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + sym + '.csv?'
        url = url + 'start_date=' + start
        url = url + '&order=asc&api_key=' + self.quandl_key
        return url

    def form_url_google(self, sym):
        dt = datetime.now()
        dt = dt.replace(year=dt.year - self.lookback)
        start = "{:%Y%m%d}".format(dt)
        url = 'http://www.google.com/finance/historical?q=' + sym
        url = url + '&startdate=' + start + '&output=csv'
        return url

    def form_url_yahoo(self, sym):
        base_url = 'http://real-chart.finance.yahoo.com/table.csv?s=' + sym
        begin_time_str = '&a=' + str(self.month - 1) + '&b=' + str(self.day - 1) + '&c=' + str(self.year - self.lookback)
        end_time_str = '&d=' + str(self.month - 1) + '&e=' + str(self.day - 1) + '&f=' + str(self.year)
        timeframe_str = '&g=d'
        return base_url + begin_time_str + end_time_str + timeframe_str + '&ignore=.csv'

    #--------------------------------------------------------------------------------------
    #   Get historical quote from Google
    #--------------------------------------------------------------------------------------
    def get_quotes_google(self, sym):

        url = self.form_url_google(sym)
        print url
        try:
            result = urlopen(url)
        except:
            print 'Request for', url, 'failed'
            return None
        else:
            lines = result.readlines()
            lines.reverse()

        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for line in lines[:-1]:
            dates.append(utils.google_quote_time_format_convert(line.split(',')[0]))

            if utils.isfloat(line.split(',')[1]): 
                open.append(float(line.split(',')[1]))
            else:
                return None

            if utils.isfloat(line.split(',')[2]):
                high.append(float(line.split(',')[2]))
            else:
                return None

            if utils.isfloat(line.split(',')[3]):
                low.append(float(line.split(',')[3]))
            else:
                return None

            if utils.isfloat(line.split(',')[4]):
                close.append(float(line.split(',')[4]))
            else:
                return None

            if utils.isint(line.split(',')[5]):
                volume.append(int(line.split(',')[5]))
            else:
                return None

        df = pd.DataFrame(index = pd.DatetimeIndex(dates))
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume

        ohlc_dict = {
            'open':'first',
            'high':'max',
            'low':'min',
            'close':'last',
            'volume':'sum'
        }

        return df

    #--------------------------------------------------------------------------------------
    #   Get historical quote from Quandl
    #--------------------------------------------------------------------------------------
    def get_quotes_quandl(self, sym):
        sym = sym.replace('-', '_')
        url = self.form_url_quandl(sym)
        print url
        try:
            result = urlopen(url)
        except:
            print 'Request for', url, 'failed'
            return None
        else:
            lines = result.read().split('\n')[1:-1]

        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for line in lines:
            if float(line.split(',')[5]) == 0.0:
                continue 
            dates.append(line.split(',')[0])
            open.append(float(line.split(',')[1]))
            high.append(float(line.split(',')[2]))
            low.append(float(line.split(',')[3]))
            close.append(float(line.split(',')[4]))
            volume.append(float(line.split(',')[5]))
    
        df = pd.DataFrame(index = dates)
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume

        return df

    #--------------------------------------------------------------------------------------
    #   Get historical quote from Yahoo
    #--------------------------------------------------------------------------------------
    def get_quotes_yahoo(self, sym):
        sym = sym.replace('.', '-')
        url = self.form_url_yahoo(sym)
        print url

    #--------------------------------------------------------------------------------------
    #   Return quote data as Pandas DataFrame object
    #--------------------------------------------------------------------------------------
    def get(self, sym, source):
        if source == 'quandl':
            return self.get_quotes_quandl(sym)
        elif source == 'google':
            return self.get_quotes_google(sym)
        elif source == 'yahoo':
            return self.get_quotes_yahoo(sym)
        else:
            return None
    
