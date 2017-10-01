import sys
import os
import json
import pandas as pd
import config
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns
from finviz import Finviz
from report import Report

DATA_DIR = config.DATA_DIR
sym_file = config.TRADABLE_STOCKS
current_sym_file = config.CUR_SYM
ibd_stock_file = config.IBD_STOCKS

class Scan:

    def __init__(self):
        self.latest_date = ''
        self.spy_df = None

    def update_quotes(self, sym_list = None):

        if sym_list is None:
            return

        q = Quote()
        self.spy_df = q.update('SPY')
        if self.spy_df is not None:
            latest_date = self.spy_df.index[-1]
        else:
            latest_date = None

        for sym in sym_list:
            df = q.update(sym, latest_date)
 
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
            if os.path.isfile(DATA_DIR + sym + '_analysis.csv'):
                analysis_df = pd.read_csv(DATA_DIR + sym + '_analysis.csv', index_col = 0)
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
                print entry
                symbol_list.append(key)

        print symbol_list
        print len(symbol_list)

        return symbol_list
