CONFIG_DIR = '../config/'
DATA_DIR = '../data/'
TRADABLE_STOCKS = '../data/tradable_stocks.txt'
CUR_SYM = '../data/cur_symbol.txt'

ACCESS_TOKEN = 0
ACCESS_SECRET = 1
CONSUMER_KEY = 2
CONSUMER_SECRET = 3

def get_twitter_keys(id):
    lines = open(CONFIG_DIR + 'twitter_key', 'r').read().split('\n')
    return lines[id]
