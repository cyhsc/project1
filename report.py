import sys
import os
import json
import pandas as pd
import config
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns
from finviz import Finviz

ANALYSIS_DIR = config.ANALYSIS_DIR
report_file = ANALYSIS_DIR + 'report.txt'

class Report:

    def __init__(self):
        pass

    def report(self, sym_list = None):
        if sym_list == None: 
            print 'Nothing to report, exit'

        wfile = open(report_file, 'w')

        for sym in sym_list:
            wfile.write('\n---------------' + sym + '---------------' + '\n')
            analysis_df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)

            wfile.write('MACD analysis:' + '\n')
            res = '    '
            macd_hist_pb = analysis_df['macd_hist_pb']            
            if macd_hist_pb[-1] == 0: 
                res = res + 'histogram < 0 and '
            else:
                res = res + 'histogram > 0 and '

            macd_hist_roc_pb = analysis_df['macd_hist_roc_pb']
            if macd_hist_roc_pb[-1] == 0: 
                res = res + 'is descreasing.' + '\n'
            else:
                res = res + 'has been increasing for ' + str(macd_hist_roc_pb[-1]) + ' bars.' + '\n'

            wfile.write(res)
        
            wfile.write('Guppy analysis:' + '\n')
            res = '    '
            swidth_pb = analysis_df['swidth_pb']
            if swidth_pb[-1] == 0: 
                res = res + 'Slow band width is negative' + '\n'
            else: 
                res = res + 'Slow band width has been positive for ' + str(swidth_pb[-1]) + ' bars.' + '\n' 
            
            wfile.write(res)

        wfile.close()
