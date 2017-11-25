import os
import sys
import time
import json
import utils
import config

ANALYSIS_DIR = config.ANALYSIS_DIR
earnings_file = ANALYSIS_DIR + 'earnings.json'

class Nasdaq:

    def __init__(self):
        pass

    def already_has_earnings(self, key, past_earnings): 
        for earning in past_earnings: 
            if key == earning[0]: 
                return True
  
        return False
   
    def earning(self, sym):

        today_str = utils.current_date_str()
        print 'Today is', today_str

        # -----------------------------------------------------------------------
        # Setting up earnings_db
        # -----------------------------------------------------------------------

        if os.path.isfile(earnings_file):
            earnings_db = json.loads(open(earnings_file, 'r').read())        
        else:
            earnings_db = {}

        if sym in earnings_db: 
            earnings = earnings_db[sym]
        else: 
            earnings_db[sym] = {}
            earnings = earnings_db[sym]

        if 'update' in earnings:
            if earnings['update'] == today_str: 
                print 'Updated today, no need to do anything'
                return False

        # -----------------------------------------------------------------------
        # Fetch the page
        # -----------------------------------------------------------------------

        url = 'http://www.nasdaq.com/earnings/report/' + sym.lower()
        print url
        soup = utils.get_url_soup_no_user_agent(url)
        earnings_div = soup.body.find('div', attrs={'id': 'left-column-div'})

        # -----------------------------------------------------------------------
        # Figure out earnings announcement date
        # -----------------------------------------------------------------------
        earnings_date = earnings_div.find('h2')
        announcement_str = earnings_date.contents[0].strip('\t').strip('\r\n').strip(' ')
        date_str = announcement_str.split(':')[1].strip(' ')
        if len(date_str) == 0: 
            print 'No earnings date yet'
        else: 
            print date_str

        earnings['upcoming'] = date_str

        # -----------------------------------------------------------------------
        # Get past earnings announcement
        # -----------------------------------------------------------------------
        if 'past_earnings' in earnings:
            pass
        else:
            earnings['past_earnings'] = []

        past_earnings = earnings['past_earnings']

        showdata_div = soup.body.find('div', attrs={'id': 'showdata-div'})
        if showdata_div is None:
            return False

        table = showdata_div.find('table')
        if table is None:
            return False

        rows = table.find_all('tr')
        if rows is None:
            return False

        if len(rows) == 0:
            return False

        rows_new = (rows[1::])[::-1]
        for row in rows_new:
            items = row.find_all('td')

            key = items[0].contents[0]

            if self.already_has_earnings(key, past_earnings):
                print 'Already has earnings for', key
                continue

            earning_table_row = []
            for item in items:
                earning_table_row.append(item.contents[0])

            past_earnings.append(earning_table_row)

        # -----------------------------------------------------------------------
        # Write out to the file
        # -----------------------------------------------------------------------
        earnings['update'] = today_str

        fp = open(earnings_file, 'w')
        fp.write(json.dumps(earnings_db, indent=4))
        fp.close()

        return True

def main(argv):

    n = Nasdaq()
    n.earning('CSCO')

if __name__ == '__main__':
    main(sys.argv[1:])

