import os
import sys
import time
import utils
import config

#
# base_url = 'http://finviz.com/screener.ashx?f=cap_midover,sh_avgvol_o300,sh_price_o10'
# other_url = 'http://finviz.com/screener.ashx?f=cap_midover,geo_usa,sh_avgvol_o300,sh_price_o10&r=21'
#

output_file = config.TRADABLE_STOCKS

class Finviz:

    def __init__(self):
        pass

    def get_total(self, soup):
        screen_content = soup.body.find('div', attrs={'id': 'screener-content'})
        table = screen_content.find('table')
        rows = table.find_all('tr', recursive = False)
        total_row_table = rows[2].find('table')
        total_row = total_row_table.find('tr')
        total_cell = total_row.find('td')
        total_cell_content = total_cell.contents[1]
        total = int(total_cell_content.split()[0])
        return total

    def get_result(self, soup):
        syms = []
        screen_content = soup.body.find('div', attrs={'id': 'screener-content'})
        table = screen_content.find('table')
        result_row = table.find_all('tr', recursive = False)[3]
        result_table = result_row.find('table')
        rows = result_table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('a')
            syms.append(cells[1].contents[0])

        return syms

    def screen(self, base_url):
        url = base_url
        soup = utils.get_url_soup(base_url)
        total = self.get_total(soup)
        sym_list = self.get_result(soup)
        print sym_list
        num = len(sym_list) + 1
        while num < total:
            url = base_url + '&r=' + str(num)
            print url
            soup = utils.get_url_soup(url)
            syms = self.get_result(soup)
            num = num + len(syms)
            print syms
            sym_list = sym_list + syms
            time.sleep(1)

        return sym_list

    def sym_list_update_to_date(self):

        if os.path.isfile(output_file):
            now = time.localtime()
            year, month, mday, wday = utils.file_modification_time(output_file)
            print now
            if (now.tm_mday > mday) or ((now.tm_mday < mday) and (now.tm_mon > month)):
                if now.tm_wday <= 5:
                    return False
                else:
                    if wday <= 4:
                        return False
                    else:
                        return True
            else:
                return True
        else:
            return False

    def get_tradable_stocks(self):
        if self.sym_list_update_to_date():
            print 'Symbol list is up to date'
        else:
            print 'Symbol list is not up to date, getting the symbol list'
            sym_list = self.screen('http://finviz.com/screener.ashx?f=cap_midover,sh_avgvol_o300,sh_price_o10')
            print 'Writing to file', output_file, '...'
            wf = open(output_file, 'w')
            for sym in sym_list:
                wf.write(sym + '\n')
   
    def get_classification(self, sym):
        url = 'http://finviz.com/quote.ashx?t=' + sym
        soup = utils.get_url_soup(url)
        table = soup.body.find_all('table', attrs={'class': 'fullview-title'})[0]
        rows = table.find_all('tr')
        entries = rows[2].find_all('a')
        return rows[1].find('b').contents[0], entries[0].contents[0], entries[1].contents[0]
