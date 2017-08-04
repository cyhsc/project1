import sys
import os
import pandas as pd
import config
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns

DATA_DIR = config.DATA_DIR

symbol = 'CSCO'

def test1(sym):
    q = Quote()
    spy_df = q.get('spy', 'google')
    df = q.get(sym, 'quandl')
    a = Analysis(sym)
    a.analysis(df, spy_df)

    if df is not None:
        df.to_csv(DATA_DIR + sym + '.csv')

def test2(sym):
    df = pd.read_csv(DATA_DIR + sym + '.csv', index_col = 0)
    a = Analysis(sym)
    a.renko(df)

def test3(sym): 
    df = pd.read_csv(DATA_DIR + sym + '_renko.csv', index_col = 0)

    p = RenkoPatterns()
    found, pattern_list = p.pattern_wbw(df)
    for item in pattern_list:
        print item
    print 'Found at last bar is', found

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):
    # --------------------------------------------------------------
    # Set Pandas print option to print all rows and columns
    # --------------------------------------------------------------
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    test1(symbol)
    test3(symbol)

if __name__ == '__main__':
    main(sys.argv[1:])
