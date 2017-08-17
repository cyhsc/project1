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
        self.spy_df = q.update('SPY')
        if self.spy_df is not None:
            latest_date = self.spy_df.index[-1]
        else:
            latest_date = None

        for sym in sym_list:
            df = q.update(sym, latest_date)
 
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
  
