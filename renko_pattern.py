import sys
import os
import pandas as pd
import config

class RenkoPatterns:

    def __init__(self):
        pass

    #-----------------------------------------------------------------------
    #  This method try to identify the following pattern
    #  multiple white, one black, multiple white [w*bw*]
    #-----------------------------------------------------------------------
    def pattern_wbw(self, df): 

        pattern_list = []
        pattern_stats = []
        pattern = []
        w1 = 0
        w2 = 0
        b = 0
        found_index = 0

        for index, row in df.iterrows():
            print index, row['date'], row['color']

            if row['color'] == 'B': 
                if w1 < 2:
                    del pattern[:]
                    w1 = 0
                    w2 = 0
                    b = 0
                elif b == 0: 
                    if w2 == 0:
                        b = b + 1
                        pattern.append([index, row['date'], row['color']])
                else:
                    if w2 > 0:
                        print '+++++++++++++ Append'
                        pattern_list.append([[w1, b, w2], pattern[:]])
                        del pattern[:(w1 + 1)]
                        pattern.append([index, row['date'], row['color']])
                        w1 = w2
                        w2 = 0
                        b = 1
                    else:
                        w1 = 0
                        w2 = 0
                        b = 0
                        del pattern[:]
                print '  - Black bar', w1, w2, b, pattern
            else:
                if b == 0:
                    w1 = w1 + 1
                elif b == 1:
                    w2 = w2 + 1
                    if w2 == 1:
                        print '------------- Found' 
                        found_index = index
                        
                pattern.append([index, row['date'], row['color']])
                print '  - White bar', w1, w2, b, pattern

        print 'Last index =', index, ', Last found index =', found_index 

        return (index == found_index), pattern_list

            
