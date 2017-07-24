import numpy as np
import talib
import math

class TechData:

    def __init__(self):
        pass

    #-------------------------------------------------------------------
    #   Calculate Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #   - period: moving average period such as 50, 200, etc.
    #-------------------------------------------------------------------
    def sma(self, data, period):
        np_closes = np.array(data['close'], dtype=float)
        data['sma' + str(period)] = talib.SMA(np_closes, timeperiod=period).tolist()

    #-------------------------------------------------------------------
    #   Calculate Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #   - period: moving average period such as 50, 200, etc.
    #-------------------------------------------------------------------
    def ema(self, data, period):
        np_closes = np.array(data['close'], dtype=float)
        data['ema' + str(period)] = talib.EMA(np_closes, timeperiod=period).tolist()

    #-------------------------------------------------------------------
    #   Calculate MACD
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def macd(self, data):
        np_closes = np.array(data['close'], dtype=float)
        macd, macd_sig, macd_hist = talib.MACD(np_closes)
        data['macd'] = macd.tolist()
        data['macd_sig'] = macd_sig.tolist()
        data['macd_hist'] = macd_hist.tolist()

    #-------------------------------------------------------------------
    #   Calculate Guppy Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def guppy(self, data):
        guppy_periods = [3, 5, 7, 10, 12, 15, 30, 35, 40, 45, 50, 60]
        np_closes = np.array(data['close'], dtype=float)
        for period in guppy_periods:
            data['ema' + str(period)] = talib.EMA(np_closes, timeperiod=period).tolist()

    #-------------------------------------------------------------------
    #   Calculate Volume Moving Averages
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def volume(self, data):
        np_volumes = np.array(data['volume'], dtype=float)
        data['vol_sma50'] = talib.SMA(np_volumes, timeperiod=50).tolist()

    #-------------------------------------------------------------------
    #   Calculate Relative Performance
    #   - data: Pandas dataframe object containing quotes
    #   - base_data: Pandas dataframe object containing quotes for base symbol
    #
    #   Assuming base_data contains more bars than data
    #-------------------------------------------------------------------
    def relative(self, data, base_data):
        closes = data['close']
        r_closes = closes[::-1]
        base_closes = base_data['close']
        r_base_closes = base_closes[::-1]

        len_closes = len(closes)
        len_base_closes = len(base_closes)
        min_len = min(len_closes, len_base_closes)
 
        rel = []
        for index in xrange(min_len):
            rel.insert(0, (r_closes[index]/r_base_closes[index]))

        data['rel'] = rel
        np_rel = np.array(rel, dtype=float)
        data['rel_ema30'] = talib.EMA(np_rel, timeperiod=30).tolist()

    #-------------------------------------------------------------------
    #   Calculate ATR
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def atr(self, data):
        np_close = np.array(data['close'], dtype=float)
        np_high= np.array(data['high'], dtype=float)
        np_low= np.array(data['low'], dtype=float)
        data['atr'] = talib.ATR(np_high, np_low, np_close, timeperiod=14)

    #-------------------------------------------------------------------
    #   Calculate Renko chart
    #   - data: Pandas dataframe object containing quotes
    #-------------------------------------------------------------------
    def renko(self, data):
        closes = data['close']
        closes_list = closes.tolist()
        renko_df = closes.to_frame()
        atr = data['atr'].tolist()[-1]
        renko_bars = [None] * len(closes_list)

        if np.isnan(atr) == False:

            for index, elem in enumerate(closes_list):
                if index == 0: 
                    high = closes_list[index]
                    low = closes_list[index]
                    renko_bars[index] = 'Base,' + str(high) + ',' + str(low)
                elif (closes_list[index] < (high + atr)) and (closes_list[index] > (low - atr)):
                    renko_bars[index] = '<'
                else: 
                    #-------------------------------------------------
                    # We need to draw some bars 
                    #-------------------------------------------------
                    if high == low:  
                        #-------------------------------------------------
                        # Drawing first bar
                        #-------------------------------------------------
                        if (closes_list[index] >= (high + atr)):
                            bars = int((closes_list[index] - high)/atr)
                            high = high + atr*bars
                            low = low + atr*(bars - 1)
                            renko_bars[index] = 'W,' + str(bars) + ',' + str(high) + ',' + str(low)
                        else:
                            bars = int((low - closes_list[index])/atr)
                            high = high - atr*(bars - 1)
                            low = low - atr*bars
                            renko_bars[index] = 'B,' + str(bars) + ',' + str(high) + ',' + str(low)
                    else:
                        #-------------------------------------------------
                        # Drawing subsequent bars 
                        #-------------------------------------------------
                        if (closes_list[index] >= (high + atr)):
                            bars = int((closes_list[index] - high)/atr)
                            high = high + atr*bars
                            low = low + atr*bars
                            renko_bars[index] = 'W,' + str(bars) + ',' + str(high) + ',' + str(low)
                        else:
                            bars = int((low - closes_list[index])/atr)
                            high = high - atr*bars
                            low = low - atr*bars
                            renko_bars[index] = 'B,' + str(bars) + ',' + str(high) + ',' + str(low)


        renko_df['renko'] = renko_bars
        data['renko'] = renko_bars
   
        #print renko_df
