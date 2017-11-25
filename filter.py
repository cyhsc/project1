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
        self.negsw = []
        self.possw = []
        self.possw_pb = []
        self.rwb = []
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

    def run(self):
      
        for sym in self.symbol_list:
            df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)

            close = df['close']
            if close[-1] < 10:
                self.sub10.append(sym)

            sw = df['swidth']
            sw_pb = df['swidth_pb']
            if sw[-1] < 0:
                self.negsw.append(sym)
            else:
                self.possw.append([sym, sw[-1]])
                self.possw_pb.append([sym, sw_pb[-1]])

                rwb = df['rwb']
                if rwb[-1] >= 0:
                    self.rwb.append(sym)

                    macd_hist_pb = df['macd_hist_pb']
                    if (macd_hist_pb[-1] > 0) and (macd_hist_pb[-1] <= 10):
                        for value in macd_hist_pb[::-1]: 
                            if value < 0: 
                                break
                        self.macd_histo_cross.append([sym, macd_hist_pb[-1], value])

        sorted_possw_pb = self.sort_possw_pb()

        #################################################################
        # Print out the results
        #################################################################

        print '-------------- Symbol List -----------------'
        print self.symbol_list
        print len(self.symbol_list)

        print '-------------- Sub10 -----------------'
        print self.sub10
        print len(self.sub10)

        print '-------------- Negative Slow Width -----------------'
        print self.negsw
        print len(self.negsw)

        print '-------------- Postive Slow Width -----------------'
        print self.possw
        print len(self.possw)

        print '-------------- Postive RWB -----------------'
        print self.rwb
        print len(self.rwb)

        print '-------------- MACD Histo Cross -----------------'
        min = 10000
        max = 0
        for item in self.macd_histo_cross:
             if item[1] < min:
                 min = item[1]
             if item[1] > max:
                 max = item[1]

        fp = open(ANALYSIS_DIR + 'filter.txt', 'w')

        print min, max
        output_str = str(min) + ', ' + str(max) + '\n'
        fp.write(output_str)

        for i in range(min, max + 1): 
            for item in self.macd_histo_cross:
                if item[1] == i:
                    print item
                    output_str = '[%s, %d, %d]\n' % (item[0], item[1], item[2])
                    fp.write(output_str)
  
        print len(self.macd_histo_cross)
        output_str = str(len(self.macd_histo_cross)) + '\n'
        fp.write(output_str)

        print '-------------- Sorted Slow Width List -----------------'
        for item in sorted_possw_pb: 
            print item
            output_str = '[%s, %d]\n' % (item[0], item[1])
            fp.write(output_str)
         
        fp.close()

