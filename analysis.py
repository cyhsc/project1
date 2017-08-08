import os
import pandas as pd
import numpy as np
from tech import TechData
import config

DATA_DIR = config.DATA_DIR

##############################################################################################
#
# This class will perform analysis 
#
##############################################################################################

class Analysis:

    def __init__(self):
        pass

    # ---------------------------------------------------
    # Calculate min/max of a data series
    # ---------------------------------------------------
    def minmax(self, data_series, ignore_nan = 0):
        initialized = 0
        min = float('NaN')
        max = float('NaN')
        for index, elem in enumerate(data_series):
            if np.isnan(elem) == False:
                if initialized == 1:
                    if elem < min:
                        min = elem
                    if elem > max:
                        max = elem
                else:
                    initialized = 1
                    min = elem
                    max = elem
            else:
                if ignore_nan == 0: 
                    min = float('NaN')
                    max = float('NaN')
                    break

        return min, max

    # ---------------------------------------------------
    #   Calculate rate of change
    # ---------------------------------------------------
    def roc(self, data_series):
        r = []
        for index, elem in enumerate(data_series):
            if index == 0:
                r.append(float('NaN'))
            else:
                r.append(elem - data_series[index - 1])
        return r

    # ---------------------------------------------------
    #   Calculate number of consecutive positive bars
    # ---------------------------------------------------
    def positive_bars(self, data_series, nonneg = True):
        r = []
        bars = 0
        for index, elem in enumerate(data_series):
            if np.isnan(elem) == True:
                bars = 0
            elif elem < 0:
                bars = 0 
            elif elem == 0: 
                if nonneg == True:
                    bars = bars + 1
                else:
                    bars = 0
            else:
                bars = bars + 1

            r.append(bars)
  
        return r

    # ---------------------------------------------------
    # Perform analysis of Guppy 
    # - Data: dataframe containing quote and tech info
    # ---------------------------------------------------
    def guppy(self, data):

        fwidth = []
        swidth = []
        rwb = []

        for index, row in data.iterrows():
            fast = [row['ema3'], row['ema5'], row['ema7'], row['ema10'], row['ema12'], row['ema15']]
            slow = [row['ema30'], row['ema35'], row['ema40'], row['ema45'], row['ema50'], row['ema60']]
            fmin, fmax = self.minmax(fast)
            smin, smax = self.minmax(slow)

            if row['ema3'] > row['ema15']:
                fwidth.append(fmax - fmin)
            else:
                fwidth.append(fmin - fmax)
        
            if row['ema30'] > row['ema60']:
                swidth.append(smax - smin)
            else:
                swidth.append(smin - smax)

            if fmin > smax: 
                rwb.append(fmin - smax)
            elif smin > fmax:
                rwb.append(fmax - smin)
            else:
                rwb.append(0.0)

        guppy_periods = [3, 5, 7, 10, 12, 15, 30, 35, 40, 45, 50, 60]
        for period in guppy_periods:
            data['ema' + str(period) + '_roc'] = self.roc(data['ema' + str(period)])
       
        data['fwidth'] = fwidth
        data['fwidth_pb'] = self.positive_bars(data['fwidth'])
        data['fwidth_roc'] = self.roc(fwidth)
        data['fwidth_roc_pb'] = self.positive_bars(data['fwidth_roc'])
        data['swidth'] = swidth
        data['swidth_pb'] = self.positive_bars(data['swidth'])
        data['swidth_roc'] = self.roc(swidth)
        data['swidth_roc_pb'] = self.positive_bars(data['swidth_roc'])
        data['rwb'] = rwb
        data['rwb_pb'] = self.positive_bars(data['rwb'])
        data['rwb_roc'] = self.roc(rwb)
        data['rwb_roc_pb'] = self.positive_bars(data['rwb_roc'])

    #-------------------------------------------------------------------
    #   MACD Analysis
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def macd(self, data):
        data['macd_roc'] = self.roc(data['macd'])
        data['macd_roc_pb'] = self.positive_bars(data['macd_roc'])
        data['macd_sig_roc'] = self.roc(data['macd_sig'])
        data['macd_sig_roc_pb'] = self.positive_bars(data['macd_sig_roc'])
        data['macd_hist_roc'] = self.roc(data['macd_hist'])
        data['macd_hist_pb'] = self.positive_bars(data['macd_hist'])

    #-------------------------------------------------------------------
    #   Renko Analysis
    #   - data: Pandas dataframe object containing quotes
    #   
    #   Output:
    #   - True Renko bars, one bar per row in data frame
    #-------------------------------------------------------------------
    def renko(self, data):

        renko_data = data['renko']
        #print renko_raw
        renko_df = pd.DataFrame(columns = ['date', 'color', 'low', 'high', 'close'])

        loc = 0
        for index, row in data.iterrows():
             if row['renko'] == '<':
                 continue
 
             if row['renko'].split(',')[0] == 'Base':
                 continue

             color = row['renko'].split(',')[0]
             count = int(row['renko'].split(',')[1])
             high = float(row['renko'].split(',')[2])
             low = float(row['renko'].split(',')[3])
             delta = high - low

             if count <= 1:
                 renko_df.loc[loc] = [index, color, low, high, (low + high)/2]
                 loc = loc + 1
             else:
                 for i in range(count):
                     if color == 'W':
                         new_low = low - (count - 1 - i)*delta
                         new_high = high - (count - 1 - i)*delta
                     else:
                         new_low = low + (count - 1 - i)*delta
                         new_high = high + (count - 1 - i)*delta

                     renko_df.loc[loc] = [index, color, new_low, new_high, (low + high)/2]
                     loc = loc + 1

        return renko_df
        
    #-------------------------------------------------------------------
    #   Overall Analysis
    #-------------------------------------------------------------------
    def analysis(self, symbol, df, ref_df):

        td = TechData()
 
        td.volume(df)
        td.macd(df)
        td.guppy(df)
        if ref_df != None:
            td.relative(df, ref_df)
        td.atr(df)
        td.renko(df)
        self.guppy(df)
        self.macd(df)

        renko_df = self.renko(df)
        td.guppy(renko_df)
        self.guppy(renko_df)
        
        if renko_df is not None:
            renko_df.to_csv(DATA_DIR + symbol + '_renko' + '.csv')
