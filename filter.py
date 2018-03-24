import sys
import os
import json
import pandas as pd
import time
import config
import utils
from report import Report

DATA_DIR = config.DATA_DIR
ANALYSIS_DIR = config.ANALYSIS_DIR
sym_file = config.TRADABLE_STOCKS
current_sym_file = config.CUR_SYM
ibd_stock_file = config.IBD_STOCKS

class Filter:

    def __init__(self):

        self.symbol_list = []
        self.sub10 = []
        self.volume_sub200k = []
        self.possw_pb = []
        self.macd_histo_cross = []
    
        filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') ]
        for f in filelist:
            sym = f.split('.')[0]
            self.symbol_list.append(sym)

    def sort_possw_pb(self): 
        
        print 'Sorting postive slow width list ...'

        result = []

        for item in self.possw_pb:
            inserted = False
            for idx, val in enumerate(result): 
                if item[1] > val[1]: 
                    continue
                else:
                    result.insert(idx, item)
                    inserted = True
                    break

            if inserted == False:
                result.append(item)

        return result 

    def find_sub10(self, symbol_list):

        print 'Filtering for stocks with close < $10 ....'

        for sym in self.symbol_list:
            df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
            close = df['close']
            if close[-1] < 10:
                self.sub10.append(sym)

    def find_volume_sub200k(self, symbol_list):

        print 'Filtering for stocks with average volume < 200k ....'      

        for sym in self.symbol_list:
            df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
            vol_sma50 = df['vol_sma50']
            if vol_sma50[-1] < 200000:
                self.volume_sub200k.append([sym, int(vol_sma50[-1])])

    def find_non_neg_slow_width(self, symbol_list):
    
        print 'Filtering for stocks with non negative slow width ....'

        possw_pb = []

        for sym in self.symbol_list:
            df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)
            sw = df['swidth']
            sw_pb = df['swidth_pb']
            if sw[-1] >= 0:
                possw_pb.append([sym, sw_pb[-1]])

        print ' - Sorting postive slow width list ...'

        for item in possw_pb:
            inserted = False
            for idx, val in enumerate(self.possw_pb):
                if item[1] > val[1]:
                    continue
                else:
                    self.possw_pb.insert(idx, item)
                    inserted = True
                    break

            if inserted == False:
                self.possw_pb.append(item)

        print ' - Add in fast width value ...'
    
        for item in self.possw_pb: 
            df = pd.read_csv(ANALYSIS_DIR + item[0] + '_analysis.csv', index_col = 0)
            fw_pb = df['fwidth_pb']
            item.append(fw_pb[-1])
            macd_hist_pb = df['macd_hist_pb']
            item.append(macd_hist_pb[-1])
        
        print ' - Writing to filter result file ...'

        fp = open(ANALYSIS_DIR + 'filter.txt', 'a')

        output_str = '-------------- Sorted Slow Width List, total = ' + str(len(self.possw_pb)) + '  -----------------\n'
        fp.write(output_str)
        print output_str

        for item in self.possw_pb:
            output_str = '[%s, %d, %d, %d]' % (item[0], item[1], item[2], item[3])
            if (item[2] > 0 and item[2] < 3 and item[3] > 0) or (item[2] > 0 and item[3] > 0 and item[3] < 3):
                output_str = output_str + ' *\n'
            else:
                output_str = output_str + '\n'
            print output_str
            fp.write(output_str)

        fp.close()

    def run(self):

        fp = open(ANALYSIS_DIR + 'filter.txt', 'w')
        output_str = '********************  Filtering Results ********************\n'
        fp.write(output_str)
        print output_str
        fp.close()

        self.find_sub10(self.symbol_list)
        self.find_volume_sub200k(self.symbol_list)
        self.find_non_neg_slow_width(self.symbol_list)
      
