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

    #------------------------------------------------------------------
    #
    #------------------------------------------------------------------
    def macd(self, analysis_df, wfile): 

        wfile.write('MACD analysis:' + '\n')
        res = '    '
        macd_hist_pb = analysis_df['macd_hist_pb']
        if macd_hist_pb[-1] < 0:
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'MACD histogram has been ' + sign + ' for ' + str(macd_hist_pb[-1]) + ' bars and '

        macd_hist_roc_pb = analysis_df['macd_hist_roc_pb']
        if macd_hist_roc_pb[-1] < 0:
            change = 'descreasing'
        else:
            change = 'increasing'

        res = res + 'has been ' + change + ' for ' + str(macd_hist_roc_pb[-1]) + ' bars.' +'\n'

        wfile.write(res)

        res = '    '
        macd = analysis_df['macd']
        if macd[-1] < 0:
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'MACD is ' + sign + ', '

        macd_sig = analysis_df['macd_sig']
        if macd_sig[-1] < 0:
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'MACD signal is ' + sign
        res = res + '\n'

        wfile.write(res)

        res = '    '
        macd_sig_roc_pb = analysis_df['macd_sig_roc_pb']
        if macd_sig_roc_pb[-1] < 0:
            change = 'decreasing' 
        else:
            change = 'increasing'

        res = res + 'MACD signal line has been ' + change + ' for ' + str(macd_sig_roc_pb[-1]) + ' bars.' + '\n'
        wfile.write(res)

    #------------------------------------------------------------------
    #
    #------------------------------------------------------------------
    def guppy(self, analysis_df, wfile): 

        wfile.write('Guppy analysis:' + '\n')
        #------------------------------------------------------------------
        # Slow Guppy Band Width
        #------------------------------------------------------------------
        res = '    '
        swidth_pb = analysis_df['swidth_pb']
        if swidth_pb[-1] < 0:
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'Slow band width has been ' + sign + ' for ' + str(swidth_pb[-1]) + ' bars, '

        swidth_roc_pb = analysis_df['swidth_roc_pb']
        if swidth_roc_pb[-1] < 0:
            change = 'decreasing'
        else:
            change = 'increasing'

        res = res + 'has been ' + change + ' for ' + str(swidth_roc_pb[-1]) + ' bars.' + '\n'

        wfile.write(res)

        #------------------------------------------------------------------
        # Fast Guppy Band Width
        #------------------------------------------------------------------
        res = '    '
        fwidth_pb = analysis_df['fwidth_pb']
        if fwidth_pb[-1] < 0:
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'Fast band width has been ' + sign + ' for ' + str(fwidth_pb[-1]) + ' bars, '

        fwidth_roc_pb = analysis_df['fwidth_roc_pb']
        if fwidth_roc_pb[-1] < 0:
            change = 'decreasing'
        else:
            change = 'increasing'

        res = res + 'has been ' + change + ' for ' + str(fwidth_roc_pb[-1]) + ' bars.' + '\n'

        wfile.write(res)

        #------------------------------------------------------------------
        # Fast Guppy Band Width
        #------------------------------------------------------------------
        res = '    '
        rwb_pb = analysis_df['rwb_pb']
        if rwb_pb[-1] < 0: 
            sign = 'negative'
        else:
            sign = 'positive'

        res = res + 'RWB has been ' + sign + ' for ' + str(rwb_pb[-1]) + ' bars.' + '\n'

        wfile.write(res)


    def report(self, sym_list = None):
        if sym_list == None: 
            print 'Nothing to report, exit'

        wfile = open(report_file, 'w')

        for sym in sym_list:

            wfile.write('\n---------------' + sym + '---------------' + '\n')
            analysis_df = pd.read_csv(ANALYSIS_DIR + sym + '_analysis.csv', index_col = 0)

            self.macd(analysis_df, wfile)
            self.guppy(analysis_df, wfile)

        wfile.close()

    def percent_mover(self):
    
        if os.path.isfile(ANALYSIS_DIR + 'percent_mover.json'):
            percent_mover = json.loads(open(ANALYSIS_DIR + 'percent_mover.json', 'r').read())
        else:
            print 'No percent_mover.json, bail'
            return

        results = []

        keys = percent_mover.keys()
        print keys
        for key in keys:
            print '-------------', key, '-------------'
            symbols = percent_mover[key]
            for sym in symbols:
                print sym
