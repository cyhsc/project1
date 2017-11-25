import os
import sys
import time
import utils
import config


class IBD:

    def __init__(self):
        self.sym2url = {}
        pass

    def basic(self, sym):

        self.sym2url['CSCO'] = 'http://research.investors.com/stock-quotes/nasdaq-cisco-systems-inc-csco.htm'
 
        url = self.sym2url['CSCO']

        print url
        soup = utils.get_url_soup(url)
        print soup
