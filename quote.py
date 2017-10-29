
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
import os
import time
import config
import utils

warnings.simplefilter(action='ignore', category=FutureWarning)

DATA_DIR = config.DATA_DIR
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

    def form_url_nasdaq(self, sym): 
        return 'http://www.nasdaq.com/symbol/' + sym.lower().replace('-', '.') + '/historical'

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

        print lines

        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for line in lines[:-1]:
            dates.append(utils.google_quote_time_format_convert(line.split(',')[0]))
            try: 
                open.append(float(line.split(',')[1]))
            except:
                open.append(line.split(',')[1])

            try: 
                high.append(float(line.split(',')[2]))
            except:
                high.append(line.split(',')[2])

            try:
                low.append(float(line.split(',')[3]))
            except:
                low.append(line.split(',')[3])

            try:
                close.append(float(line.split(',')[4]))
            except:
                close.append(line.split(',')[4])

            try:
                volume.append(int(line.split(',')[5]))
            except:
                volume.append(line.split(',')[5])

        df = pd.DataFrame(index = pd.DatetimeIndex(dates))
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume

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
    #   Get historical quote from Nasdaq
    #--------------------------------------------------------------------------------------
    def get_quotes_nasdaq(self, sym):
        url = self.form_url_nasdaq(sym)
        print url
        try: 
            soup = utils.get_url_soup(url)
        except:
            print 'Request for', url, 'failed'
            return None

        quote_div = soup.body.find('div', attrs={'id': 'historicalContainer'})
        tbody = quote_div.find('tbody')
        if tbody is None: 
            return None
        tr = tbody.find_all('tr')
        lines = []
        for item in tr:
            td = item.find_all('td')
            line = []
            for i in td:
                tokens = i.contents[0].splitlines()
                if (len(tokens) == 1) or (tokens[1] == ''):
                    continue
                line.append(tokens[1].strip())

            lines.append(line)

        lines = lines[::-1]

        dates = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        for line in lines:
            if len(line) == 0:
                continue
            if line[0] == '16:00': 
                #dates.append(time.strftime('%Y-%m-%d'))
                continue
            else: 
                tmp = line[0].split('/')
                dates.append(tmp[2] + '-' + tmp[0] + '-' + tmp[1])
            open.append(float(line[1].replace(',', '')))
            high.append(float(line[2].replace(',', '')))
            low.append(float(line[3].replace(',', '')))
            close.append(float(line[4].replace(',', '')))
            volume.append(int(line[5].replace(',', '')))

        df = pd.DataFrame(index = dates)
        df['open'] = open
        df['high'] = high
        df['low'] = low
        df['close'] = close
        df['volume'] = volume

        return df

    #--------------------------------------------------------------------------------------
    #   Return quote data as Pandas DataFrame object
    #--------------------------------------------------------------------------------------
    def get(self, sym, source):
        if source == 'quandl':
            df = self.get_quotes_quandl(sym)
        elif source == 'google':
            df = self.get_quotes_google(sym)
        elif source == 'nasdaq':
            df = self.get_quotes_nasdaq(sym)
        else:
            df = None
    
        if df is not None:
            if df.empty: 
                df = None

        return df

    #--------------------------------------------------------------------------------------
    #   Update quote data 
    #--------------------------------------------------------------------------------------
    def update(self, sym, latest_date = None):
        if os.path.isfile(DATA_DIR + sym + '.csv'): 
            df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)

            print latest_date, df.index[-1]

            if latest_date is None or df.index[-1] < latest_date:
                nasdaq_df = self.get(sym, 'nasdaq')
                if nasdaq_df is None:
                    return

                latest_date = nasdaq_df.index[-1]
          
            print 'Symbol:', sym, ', Last index =', df.index[-1], ', Latest =', latest_date

            if df.index[-1] < latest_date:
                while nasdaq_df.index[0] <= df.index[-1]:
                    nasdaq_df = nasdaq_df.drop(nasdaq_df.index[0])

                if nasdaq_df.empty is False:
                    df = df.append(nasdaq_df)
            else:
                print 'Quote data already up to date'
        else:
            df = self.get(sym, 'google')
            if df is None: 
                df = self.get(sym, 'quandl')

        if df is not None: 
            df.to_csv(DATA_DIR + sym + '.csv')

        return df

    #--------------------------------------------------------------------------------------
    #   Sanitize quote data
    #--------------------------------------------------------------------------------------
    def sanitize(self, sym):
        if os.path.isfile(DATA_DIR + sym + '.csv') is False:
            print 'Symbol', sym, 'quote file does not exist????'
            return

        df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)

        bad_entry_index = []

        for i in df.index:
            #print i, df.ix[i, 'open'], df.ix[i, 'high'], df.ix[i, 'low'], df.ix[i, 'close'], df.ix[i, 'volume']
            if df.ix[i, 'open'] == '-' or df.ix[i, 'high'] == '-' or df.ix[i, 'low'] == '-' or df.ix[i, 'close'] == '-':
                bad_entry_index.append(i)

        if len(bad_entry_index) == 0:
            print 'No bad entries, done'
            return

        print 'Have bad entries ....'
        print bad_entry_index
        nasdaq_df = self.get(sym, 'nasdaq')        
        if nasdaq_df is None:
            print 'Cannot get quote data from Nasdaq ???'
            return
 
        for i in bad_entry_index:
            print i, nasdaq_df.ix[i, 'open'], nasdaq_df.ix[i, 'high'], nasdaq_df.ix[i, 'low'], nasdaq_df.ix[i, 'close']
                
            if df.ix[i, 'open'] == '-':
                df.ix[i, 'open'] = str(nasdaq_df.ix[i, 'open'])
            if df.ix[i, 'high'] == '-':
                df.ix[i, 'high'] = str(nasdaq_df.ix[i, 'high'])
            if df.ix[i, 'low'] == '-':
                df.ix[i, 'low'] = str(nasdaq_df.ix[i, 'low'])
            if df.ix[i, 'close'] == '-':
                df.ix[i, 'close'] = str(nasdaq_df.ix[i, 'close'])

        print 'Writing to file ...'
        df.to_csv(DATA_DIR + sym + '.csv')
           
    def dedupe_index(self, sym):
        if os.path.isfile(DATA_DIR + sym + '.csv') is False:
            print 'Symbol', sym, 'quote file does not exist????'
            return

        df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)
        ddf = df.reset_index().drop_duplicates(subset='index', keep='last').set_index('index')
            
        #print ddf
        print 'Writing deduped quote for', sym, 'to file ...'
        ddf.to_csv(DATA_DIR + sym + '.csv')

    def dedupe_index_all(self):

        filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
        for f in filelist:
            sym = f.split('.')[0]
            self.dedupe_index(sym)
        
        
