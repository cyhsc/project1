import sys
import os
import pandas as pd
import config
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns
from finviz import Finviz

DATA_DIR = config.DATA_DIR
sym_file = config.TRADABLE_STOCKS
current_sym_file = config.CUR_SYM

class Scan:

    def __init__(self):
        self.latest_date = ''
        self.spy_df = None

    def update_quotes(self, sym_list = None):

        if sym_list is None:
            return

        q = Quote()

        self.spy_df = q.get('spy', 'google')
        if self.spy_df is not None:
            self.spy_df.to_csv(DATA_DIR + 'spy' + '.csv')
        else:
            print 'Cannot get quote for SPY'
            print self.spy_df

        for sym in sym_list:
            df = q.get(sym, 'google')
            if df is not None: 
                df.to_csv(DATA_DIR + sym + '.csv')
            else:
                df = q.get(sym, 'quandl')
                if df is not None:
                    df.to_csv(DATA_DIR + sym + '.csv')
                else:
                    print 'Cannot get quote for', sym
 
    def update_analysis(self):

        a = Analysis()

        analysis_files = [ f for f in os.listdir(DATA_DIR) if f.endswith('_analysis.csv') ]
        for f in analysis_files:
            os.remove(DATA_DIR + f)

        renko_files = [ f for f in os.listdir(DATA_DIR) if f.endswith('_renko.csv') ]
        for f in renko_files:
            os.remove(DATA_DIR + f)

        filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
        for f in filelist:
            sym = f.split('.')[0]
            print 'Analysing', sym, '....'
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

        self.update_quotes(symbol_list) 
        self.update_analysis() 
  
