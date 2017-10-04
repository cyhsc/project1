import sys
import os
from scan import Scan
from tweets import Tweets
import config

DATA_DIR = config.DATA_DIR

def update_tweets():
    t = Tweets()
    t.update()
    t.process()

def perform_scan():

    symbols = []

    filelist = [ f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and not f.endswith('_analysis.csv') and not f.endswith('_renko.csv')]
    for f in filelist:
        sym = f.split('.')[0]
        if sym != 'SPY':
            symbols.append(sym)

    sc = Scan()
    sc.run(symbols)

# ==============================================================================
#   Main
# ==============================================================================
def main(argv):

    if len(argv) < 1: 
        print 'Dont know what task to run'
        return

    if len(argv) > 1: 
        print 'Too many arguments'
        return

    if argv[0] == '-t':
        update_tweets()
        return

    if argv[0] == '-s':
        perform_scan()
        return

if __name__ == '__main__':
    main(sys.argv[1:])
