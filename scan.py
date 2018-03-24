import sys
import os
import json
import pandas as pd
import time
import config
import utils
import random
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns
from finviz import Finviz
from report import Report
from yahoo import Yahoo
from nasdaq import Nasdaq

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR
sym_file = config.TRADABLE_STOCKS
current_sym_file = config.CUR_SYM
ibd_stock_file = config.IBD_STOCKS
earnings_file = ANALYSIS_DIR + 'earnings.json'

class Scan:

    def __init__(self, last_date = None):
        self.latest_date = ''
        self.spy_df = None
        self.last_date = last_date

    def get_analysis_df(self, sym):
        analysis_df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
        return analysis_df

    def get_quote_symbol_list(self):

        quote_symbol_list = []

        filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
        for f in filelist:
            sym = f.split('.')[0]
            quote_symbol_list.append(sym)

        return quote_symbol_list

    def get_analysis_symbol_list(self):

        analysis_symbol_list = []

        filelist = [ f for f in os.listdir(ANALYSIS_DIR) if f.endswith('.csv') and not f.endswith('_renko.csv')]
        for f in filelist:
            sym = f.split('.')[0]
            analysis_symbol_list.append(sym.replace('_analysis', ''))

        return analysis_symbol_list

    def update_quotes(self, sym_list = None):

        if sym_list is None:
            return

        q = Quote(self.last_date)
        self.spy_df, already_up_to_date = q.update('SPY')
        if self.spy_df is not None:
            latest_date = self.spy_df.index[-1]
        else:
            latest_date = None

        for sym in sym_list:
            df, already_up_to_date = q.update(sym, latest_date)
            if already_up_to_date == False:
                time.sleep(random.randint(1, 5))
 
    def update_analysis(self, symbol_list = None):

        a = Analysis()

        analysis_symbol_list = []

        if symbol_list != None:
            for sym in symbol_list: 
                analysis_symbol_list.append(sym)
        else:
            filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and not f.endswith('_analysis.csv') and not f.endswith('_renko.csv')]
            for f in filelist:
                sym = f.split('.')[0]
                analysis_symbol_list.append(sym)

        for sym in analysis_symbol_list:
            print 'Analysing', sym, '....'
            if os.path.isfile(ANALYSIS_DIR + sym + '_analysis.csv'):
                analysis_df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
                if analysis_df.empty is False: 
                    if analysis_df.index[-1] == self.latest_date:
                        continue
            if os.path.isfile(DATA_DIR + sym + '.csv'):
                f = sym + '.csv'
                df = pd.read_csv(DATA_DIR + f, index_col = 0)
                a.analysis(sym, df, self.spy_df)     

    def run(self, symbol_list = None):
  
        if symbol_list == None: 
            symbol_list = []
            lines = open(config.TRADABLE_STOCKS, 'r').read().split('\n')
            for line in lines:
                if len(line) > 0:
                    symbol_list.append(line)

        if len(symbol_list) == 0: 
            print 'Symbol list is empty, so nothing is being done'
            return

        # --------------------------------------------------------------------- 
        # Read in existing SPY quote file if exists
        # --------------------------------------------------------------------- 
        if os.path.isfile(DATA_DIR + 'SPY.csv'):
            print 'read spy.csv'
            self.spy_df = pd.read_csv(DATA_DIR + 'SPY.csv', index_col = 0)
            if self.spy_df is not None:
                self.latest_date = self.spy_df.index[-1]
            else:
                self.latest_date = None

        self.update_quotes(symbol_list) 
        self.update_analysis(symbol_list) 

        r = Report()
        r.report(symbol_list)
  
    def ibd_watch_list(self, type):
 
        #
        # 'ibd 50'
        # 'ibd spotlight'
        # 'ibd relative strength'
        #

        if os.path.isfile(ibd_stock_file):
            fp = open(ibd_stock_file, 'r')
            stocks = json.loads(fp.read())
            fp.close()
        else:
            stocks = {}
        
        #print json.dumps(stocks, indent=4)

        symbol_list = []
        for key in stocks.keys():
            entry = stocks[key];
            if type in entry.keys():
                # print entry[type]
                symbol_list.append([key, entry[type][-1]])

        for sym in symbol_list:
            print sym
        print len(symbol_list)

        diff_list = []
        quote_symbol_list = self.get_quote_symbol_list()
        for sym in symbol_list:
            if sym[0] not in quote_symbol_list:
                diff_list.append(sym)

        print '=============  Diff List ============='
        print len(diff_list)
        for sym in diff_list:
            print sym

        return symbol_list

    def percent_change_one_symbol(self, sym, pc, vr):

        df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
        closes = df['close']
        last_close = closes[-1]
        before_last_close = closes[-2]
        percent_change = ((last_close - before_last_close)/before_last_close) * 100
        volume = df['volume']
        vol_sma50 = df['vol_sma50']
        volume_ratio = float(volume[-1])/float(vol_sma50[-1])
        rwb = df['rwb']
        output_str = sym + ': last_close = ' + str(last_close) + ', before_last_close = ' + str(before_last_close)
        output_str = output_str + ', percent_change = ' + str(percent_change) + '%'
        output_str = output_str + ', volume_ratio = ' + str(volume_ratio) + ', rwb = ' + str(rwb[-1])
        if (percent_change >= pc) and (volume_ratio >= vr) and (rwb[-1] >= 0): 
            output_str = output_str + ', keep'
            result = [sym, percent_change, volume_ratio]
        else:       
            output_str = output_str + ', pass'
            result = None

        print output_str
        return result

    def percent_change(self, pc, vr, symbol_list = None):

        df = pd.read_csv(DATA_DIR + 'SPY.csv', index_col = 0)
        index = df.index
        date_string = index[-1]
        print 'Today is', date_string
        
        if os.path.isfile(ANALYSIS_DIR + 'percent_mover.json'):
            percent_mover = json.loads(open(ANALYSIS_DIR + 'percent_mover.json', 'r').read())
        else:
            percent_mover = {}

        if date_string in percent_mover.keys():
            print 'Already scanned, do nothing'
            return
        else:
            print 'Have not scanned today, scanning ...'

        scan_symbol_list = []

        if symbol_list != None:
            for sym in symbol_list:
                scan_symbol_list.append(sym)
        else:
            filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
            for f in filelist:
                sym = f.split('.')[0]
                scan_symbol_list.append(sym)

        if len(scan_symbol_list) == 0: 
            print 'Symbol list is empty, nothing to scan'

        result = []
        for sym in scan_symbol_list:
            ret = self.percent_change_one_symbol(sym, pc, vr)
            if ret != None: 
                result.append(ret)

        percent_mover[date_string] = result

        fp = open(ANALYSIS_DIR + 'percent_mover.json', 'w')
        fp.write(json.dumps(percent_mover, indent=4))
        fp.close()

        if len(result) == 0: 
            print 'Scan result emtpy'
            return None
        else:
            for item in result:
                print item

        return result

    def earnings(self, symbol_list = None): 

        scan_symbol_list = []

        if symbol_list != None:
            for sym in symbol_list:
                scan_symbol_list.append(sym)
        else:
            filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
            for f in filelist:
                sym = f.split('.')[0]
                scan_symbol_list.append(sym)

        if os.path.isfile(earnings_file):
            earnings_db = json.loads(open(earnings_file, 'r').read())
        else:
            earnings_db = {}

        n = Nasdaq()
        for sym in scan_symbol_list:
            if n.earning(sym) == True:
                time.sleep(1)

