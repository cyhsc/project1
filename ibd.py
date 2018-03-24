import os
import sys
import time
import utils
import config


class IBD:

    def __init__(self):
        self.sym2url = {}
        self.sym2url['CSCO'] = 'https://research.investors.com/stock-quotes/nasdaq-cisco-systems-inc-csco.htm'

    def basic(self, sym):
 
        url = self.sym2url['CSCO']
        print url
        soup = utils.get_url_soup(url)

        #print soup

        stock_content = soup.body.find('div', attrs={'class': 'stockContent'})
        print stock_content
        
        company_content = soup.body.find('div', attrs={'class': 'companyContent'})
        print company_content

        group_leaderships = soup.body.find_all('div', attrs={'class': 'group_leadership_block'})
        print group_leaderships[0]
        print group_leaderships[1]

def main(argv):

    i = IBD()
    i.basic('CSCO')

if __name__ == '__main__':
    main(sys.argv[1:])
