import time
import json
import os
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import utils
import config

TWEETS_DIR = config.TWEETS_DIR
scrn_name_file = config.SCRN_NAMES
ibd_stock_file = config.IBD_STOCKS

#=========================================================================================================
# 
#=========================================================================================================
class TweetMessages:
    def __init__(self):
        pass

    def process(self, msg):
        text = msg.split(',')[2]    
        words = text.split(' ')
        #print words
        
        if words[0] == 'IBD': 
            self.process_ibd(msg)

    #=========================================================
    # Process ibd info 
    #=========================================================
    def process_ibd(self, msg):

        print ibd_stock_file

        if os.path.isfile(ibd_stock_file):
            fp = open(ibd_stock_file, 'r')
            stocks = json.loads(fp.read())
            fp.close()
        else:
            stocks = {}

        words = msg.split(',')[2].split(' ')
        if words[1] == '50':
            self.process_ibd_50(msg, stocks)
        elif words[1].lower() == 'big' and words[2].lower() == 'cap':
            self.process_ibd_big_cap(msg, stocks)
        #elif words[1].lower() == 'new' and words[2].lower() == 'high':
        #    self.process_ibd_new_highs(msg, stocks)
        elif words[1].lower() == 'relative' and words[2].lower() == 'strength':
            self.process_ibd_relative_strength(msg, stocks)
        elif words[1].lower() == 'stock' and words[2].lower() == 'spotlight':
            self.process_ibd_spotlight(msg, stocks)

        if len(stocks) > 0: 
            j = json.dumps(stocks, indent=4)
            fp = open(ibd_stock_file, 'w')
            fp.write(j)
            fp.close()
            

    def process_ibd_50(self, msg, stocks):

        print 'Process IBD 50'

        date = msg.split(',')[1]
        words = msg.split(',')[2].split(' ')
        url = words[-1]
        print date, url
        soup = utils.get_url_soup(url)
        list = soup.body.find('p', attrs={'id': 'posttext'})
        items = list.contents
        for idx, item in enumerate(items):
            if (idx == 0) or (idx % 2 == 1) or len(item) < 2:
                continue
             
            num = item.lstrip('\n').split('\t')[0]
            sym = item.lstrip('\n').split('\t')[1]
            name = item.lstrip('\n').split('\t')[2]
 
            print sym, name
 
            if sym in stocks.keys():
                entry = stocks[sym]
                if name not in entry.keys():
                    entry['name'] = name
                if 'ibd 50' in entry.keys():
                    if date not in entry['ibd 50']:
                        entry['ibd 50'].append(date)
                else:
                    entry['ibd 50'] = [date]
            else:
                entry = {}
                entry['name'] = name
                entry['ibd 50'] = [date]
                stocks[sym] = entry

    def process_ibd_big_cap(self, msg, stocks):

        print 'Process IBD Big Cap'

        date = msg.split(',')[1]
        words = msg.split(',')[2].split(' ')
        print date, words
        for item in words: 

            if len(item) < 1: 
                continue

            if item[0] != '$': 
                continue

            sym = item.lstrip('$')
            print sym

            if sym in stocks.keys():
                entry = stocks[sym]
                if 'ibd big cap' in entry.keys():
                    if date not in entry['ibd big cap']:
                        entry['ibd big cap'].append(date)
                else:
                    entry['ibd big cap'] = [date]
            else:
                entry = {}
                entry['ibd big cap'] = [date]
                stocks[sym] = entry

    def process_ibd_new_highs(self, msg, stocks):

        print 'Process IBD New Highs'

        date = msg.split(',')[1]
        words = msg.split(',')[2].split(' ')
        url = words[-1]
        print date, url
        soup = utils.get_url_soup(url)
        list = soup.body.find('p', attrs={'id': 'posttext'})
        items = list.contents

        for idx, item in enumerate(items):
            if (idx == 0) or (idx % 2 == 1) or len(item) < 2:
                continue

            num = item.lstrip('\n').split('\t')[0]
            sym = item.lstrip('\n').split('\t')[1]
            name = item.lstrip('\n').split('\t')[2]

            print sym, name

            if sym in stocks.keys():
                entry = stocks[sym]
                if name not in entry.keys():
                    entry['name'] = name
                if 'ibd new highs' in entry.keys():
                    if date not in entry['ibd new highs']:
                        entry['ibd new highs'].append(date)
                else:
                    entry['ibd new highs'] = [date]
            else:
                entry = {}
                entry['name'] = name
                entry['ibd new highs'] = [date]
                stocks[sym] = entry

    def process_ibd_relative_strength(self, msg, stocks):

        print 'Process IBD Relative Strength'

        date = msg.split(',')[1]
        words = msg.split(',')[2].split(' ')
        url = words[-1]
        print date, url
        soup = utils.get_url_soup(url)
        list = soup.body.find('p', attrs={'id': 'posttext'})
        items = list.contents

        for idx, item in enumerate(items):
            if (idx == 0) or (idx % 2 == 1) or len(item) < 2:
                continue

            num = item.lstrip('\n').split('\t')[0]
            sym = item.lstrip('\n').split('\t')[1]
            name = item.lstrip('\n').split('\t')[2]

            print sym, name

            if sym in stocks.keys():
                entry = stocks[sym]
                if name not in entry.keys():
                    entry['name'] = name
                if 'ibd relative strength' in entry.keys():
                    if date not in entry['ibd relative strength']:
                        entry['ibd relative strength'].append(date)
                else:
                    entry['ibd relative strength'] = [date]
            else:
                entry = {}
                entry['name'] = name
                entry['ibd relative strength'] = [date]
                stocks[sym] = entry

    def process_ibd_spotlight(self, msg, stocks):

        print 'Process IBD Stock Spotlight'

        date = msg.split(',')[1]
        words = msg.split(',')[2].split(' ')
        url = words[-1]
        print date, url
        soup = utils.get_url_soup(url)
        list = soup.body.find('p', attrs={'id': 'posttext'})
        items = list.contents

        for idx, item in enumerate(items):
            if (idx == 0) or (idx % 2 == 1) or len(item) < 2:
                continue

            num = item.lstrip('\n').split('\t')[0]
            sym = item.lstrip('\n').split('\t')[1]
            name = item.lstrip('\n').split('\t')[2]
        
            print sym, name

            if sym in stocks.keys():
                entry = stocks[sym]
                if name not in entry.keys():
                    entry['name'] = name
                if 'ibd spotlight' in entry.keys():
                    if date not in entry['ibd spotlight']:
                        entry['ibd spotlight'].append(date)
                else:
                    entry['ibd spotlight'] = [date]
            else:
                entry = {}
                entry['name'] = name
                entry['ibd spotlight'] = [date]
                stocks[sym] = entry


#=========================================================================================================
# 
#=========================================================================================================
class Tweets:
    def __init__(self):
        self.access_token = config.get_twitter_keys(config.ACCESS_TOKEN) 
        self.access_secret = config.get_twitter_keys(config.ACCESS_SECRET)
        self.consume_key = config.get_twitter_keys(config.CONSUMER_KEY)
        self.consume_secret = config.get_twitter_keys(config.CONSUMER_SECRET)        
        self.oauth = OAuth(self.access_token, self.access_secret, self.consume_key, self.consume_secret)
        self.twitter = Twitter(auth=self.oauth, retry=True)
        self.last_id = 0

    def get_home_timeline(self, cnt = 500):
        print 'Get home timeline'
        return self.twitter.statuses.home_timeline(count = cnt)

    def get_user_timeline(self, scrn_name, cnt = 500):
        print 'Get timeline from', scrn_name
        return self.twitter.statuses.user_timeline(screen_name = scrn_name, count = cnt)

    def update(self): 

        #=========================================================
        # Read in the screen names we want to follow
        #=========================================================
        names = open(scrn_name_file, 'r').read().split('\n')

        #=========================================================
        # Loop through all the screen names 
        #=========================================================
        for name in names:
            if len(name) < 1: 
                continue
            
            #=========================================================
            # Get the tweet file if any
            #=========================================================
            print name
            filename = TWEETS_DIR + name + '.txt'

            if os.path.isfile(filename):
                rfile = open(filename, 'r')
                old_items = rfile.read().split('\n')
                rfile.close()
                print old_items
            else:
                old_items = []


            #=========================================================
            # Find the last tweet id we have seen
            #=========================================================
            last_id = 0
            if len(old_items) > 0:
                if len(old_items[-1]) < 1: 
                    old_items = old_items[:-1]
            
                last_id = int(old_items[-1].split(',')[0])

            print 'last_id =', last_id, '\n'

            #=========================================================
            # Get the tweet, if new, append to the old ones
            #=========================================================
            items = self.get_user_timeline(name, 100)
            new_item_found = 0
            new_items = []
            for item in items[::-1]:
                id = item['id']
                if id > last_id:
                    new_item_found = 1
                    text = item['text'].replace('\n', ' ')
                    output_text = (str(item['id']) + ',' + item['created_at'] + ',' + text + '\n').encode('utf8', 'replace')
                    print 'Append new itme', output_text
                    new_items.append(output_text)

            #=========================================================
            # Save the tweets
            #=========================================================
            if new_item_found == 1:
                wfile = open(filename, 'a')
                for item in new_items:
                    wfile.write(item)
                wfile.close()


    def process(self):

        #=========================================================
        # Read in the screen names we want to follow
        #=========================================================
        names = open(scrn_name_file, 'r').read().split('\n')

        #=========================================================
        # Loop through all the screen names
        #=========================================================
        tm = TweetMessages()

        for name in names:
            if len(name) < 1:
                continue

            #=========================================================
            # Get the tweet file if any
            #=========================================================
            filename = TWEETS_DIR + name + '.txt'

            if os.path.isfile(filename):
                print 'Process tweet file', filename
                rfile = open(filename, 'r')
                items = rfile.read().split('\n')
                rfile.close()
            else:
                print 'Tweet file', filename, 'doesnt exist'
                continue

            #=========================================================
            # Go through each tweet message
            #=========================================================
            last_item = ''
            for item in items: 
                if len(item) < 1: 
                    continue
  
                tm.process(item)
                last_item = item
        
