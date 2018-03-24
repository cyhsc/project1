import sys
import os
from scan import Scan
from tweets import Tweets
from filter import Filter
import config

DATA_DIR = config.DATA_DIR

def update_tweets():
    t = Tweets()
    t.update()
    t.process()

def perform_scan(last_date):

    symbols = []

    filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and not f.endswith('_analysis.csv') and not f.endswith('_renko.csv')]
    for f in filelist:
        sym = f.split('.')[0]
        if sym != 'SPY':
            symbols.append(sym)

    sc = Scan(last_date)
    sc.run(symbols)
    sc.percent_change(3.0, 1.5)

    f = Filter()
    f.run()

def perform_percent_change_scan():
    sc = Scan()
    sc.percent_change(3.0, 1.5)

def perform_filter():
    f = Filter()
    f.run()

def perform_earnings_scan():
    sc = Scan()
    sc.earnings()

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    if len(argv) < 1: 
        print 'Dont know what task to run'
        return

    if argv[0] == '-t':
        update_tweets()
        return

    if argv[0] == '-s':
        if len(argv) == 2:
            last_date = argv[1]
        else:
            last_date = None
        perform_scan(last_date)
        return

    if argv[0] == '-p':
        perform_percent_change_scan()
        return

    if argv[0] == '-f':
        perform_filter()
        return

    if argv[0] == '-e':
        perform_earnings_scan()
        return


if __name__ == '__main__':
    main(sys.argv[1:])
