import time
import json
import os
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import utils
import config

TWEETS_DIR = config.TWEETS_DIR
scrn_name_file = config.SCRN_NAMES

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

            rfile = open(filename, 'r')
            old_items = rfile.read().split('\n')
            rfile.close()
            print old_items


            #=========================================================
            # Find the last tweet id we have seen
            #=========================================================
            last_id = 0
            if len(old_items[-1]) < 1: 
                old_items = old_items[:-1]
            
            last_id = int(old_items[-1].split(',')[0])
            print 'last_id =', last_id, '\n'

            #=========================================================
            # Get the tweet, if new, append to the old ones
            #=========================================================
            items = self.get_user_timeline(name, 100)
            new_item_found = 0
            for item in items[::-1]:
                id = item['id']
                if id > last_id:
                    new_item_found = 1
                    text = item['text'].replace('\n', ' ')
                    output_text = (str(item['id']) + ',' + item['created_at'] + ',' + text + '\n').encode('utf8', 'replace')
                    print 'Append new itme', output_text
                    old_items.append(output_text)

            #=========================================================
            # Save the tweets
            #=========================================================
            if new_item_found == 1:
                wfile = open(filename, 'w')
                for item in old_items:
                    wfile.write(item)
                wfile.close()



