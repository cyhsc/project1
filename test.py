import sys
import os
import pandas as pd
import config
from quote import Quote
from analysis import Analysis
from renko_pattern import RenkoPatterns
from finviz import Finviz
from scan import Scan
from tweets import Tweets

DATA_DIR = config.DATA_DIR
sym_file = config.TRADABLE_STOCKS
cur_sym_file = config.CUR_SYM

symbol = 'SPY'

#-------------------------------------------------
# Read in all the symbols from file
#-------------------------------------------------
def get_tradable_stocks():
    symbols = []
    lines = open(sym_file, 'r').read().split('\n')
    for line in lines:
        if len(line) > 0:
            symbols.append(line.split(',')[0])
    return symbols

def test1(sym):
    q = Quote()
    df = q.get(sym, 'nasdaq')
    #a = Analysis()
    #a.analysis(sym, df, spy_df)
   
    print df

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

def test4():
    fv = Finviz()
    fv.get_tradable_stocks()
    name, sector, industry = fv.get_classification('CSCO')
    print 'Name:', name 
    print 'Sector:', sector 
    print 'Industry:', industry

def test5():
    symbol_list = [] 
    lines = open(config.TRADABLE_STOCKS, 'r').read().split('\n')
    for line in lines:
        if len(line) > 0:
            symbol_list.append(line)

    #symbol_list = ['CSCO']

    q = Quote()
    a = Analysis()
    p = RenkoPatterns()
    spy_df = q.get('spy', 'google')

    for sym in symbol_list:
        df = q.get(sym, 'google')
        if df is not None:
            a.analysis(sym, df, spy_df)
            df.to_csv(DATA_DIR + sym + '.csv')

def test6():
    sc = Scan()
    sc.run()

def test7():
    q = Quote()
    q.update('SPY')

def test8():
    q = Quote()
    filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and not f.endswith('_analysis.csv') and not f.endswith('_renko.csv')]
    for f in filelist:
        sym = f.split('.')[0]
        if sym == 'SPY': 
            continue
        print 'Analysing', sym, '....'
        df = pd.read_csv(DATA_DIR + f, index_col = 0)
        
        if df.loc['2017-07-31']['open'] == '-' or df.loc['2017-07-31']['high'] == '-' or df.loc['2017-07-31']['low'] == '-' or df.loc['2017-07-31']['close'] == '-':
            ndf = q.get(sym, 'nasdaq')
            print df.loc['2017-07-31']
            print ndf.loc['2017-07-31']

            df.replace(df.loc['2017-07-31'], ndf.loc['2017-07-31'], True)
            print df.loc['2017-07-31']
            print ndf.loc['2017-07-31']
            df.to_csv(DATA_DIR + sym + '.csv')

def test9():

    t = Tweets()
    t.update()

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

    #test1(symbol)
    #test3(symbol)
    #test4()
    #test5()
    #test6()
    #test7()
    #test8()
    test9()

if __name__ == '__main__':
    main(sys.argv[1:])
