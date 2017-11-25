import os
import sys
import time
import utils
import config

class WSJ:

    def __init__(self):
        pass

    def basic(self, sym): 

        url = 'http://quotes.wsj.com/' + sym.upper()
        print url
        soup = utils.get_url_soup(url)
        print soup
        
