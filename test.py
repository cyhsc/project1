import sys
import os
import pandas as pd
from quote import Quote
from analysis import Analysis

data_dir = 'data/'
symbol = 'CSCO'

def test1(sym):
    q = Quote()
    spy_df = q.get('spy', 'google')
    df = q.get(sym, 'google')
    a = Analysis()
    a.analysis(df, spy_df)

    if df is not None:
        df.to_csv(data_dir + sym + '.csv')

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

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    test1(symbol)

    df = pd.read_csv('data/' + symbol + '.csv')
    print df

if __name__ == '__main__':
    main(sys.argv[1:])
