import time
from time import gmtime, strftime
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import datetime
import os.path
import json

MASTER_DATA_FILE = 'master_data.json'

##############################################################################################
#
#    Time and Date related functions
#
##############################################################################################

# ----------------------------------------------------------------
#            Get current date and time
# Directive     Meaning
# %a    Weekday name.
# %A    Full weekday name.
# %b    Abbreviated month name.
# %B    Full month name.
# %c    Appropriate date and time representation.
# %d    Day of the month as a decimal number [01,31].
# %H    Hour (24-hour clock) as a decimal number [00,23].
# %I    Hour (12-hour clock) as a decimal number [01,12].
# %j    Day of the year as a decimal number [001,366].
# %m    Month as a decimal number [01,12].
# %M    Minute as a decimal number [00,59].
# %p    Equivalent of either AM or PM.
# %S    Second as a decimal number [00,61].
# %U    Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
#       All days in a new year preceding the first Sunday are considered to be in week 0.
# %w    Weekday as a decimal number [0(Sunday),6].
# %W    Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
#       All days in a new year preceding the first Monday are considered to be in week 0.
# %x    Appropriate date representation.
# %X    Apropriate time representation.
# %y    Year without century as a decimal number [00,99].
# %Y    Year with century as a decimal number.
# %Z    Time zone name (no characters if no time zone exists).
# %%    A literal '%' character.
# ----------------------------------------------------------------
def date_and_time():
    now = time
    return int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), now.strftime("%A")

def current_date_time_str():
    return strftime("%Y-%m-%d %H:%M:%S")

def current_date_str():
    return strftime("%Y-%m-%d")

def date_to_weekday(s): 
    
    # Assuming date string is of the form yyyy-mm-dd 

    l = s.split('-')
    d = datetime.date(int(l[0]), int(l[1]), int(l[2]))
    return d.strftime('%A')

def days_in_month(year, month): 

    # Assuming year and month are in string form yyyy, mm

    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_days = days[int(month) - 1]
    if int(month) == 2 and int(year) % 4 == 0:
        month_days = month_days + 1

    return month_days

def days_in_year(year): 

    # Assuming year is in string form yyyy
    year_days = 365
    if int(year) % 4 == 0: 
        year_days = year_days + 1

    return year_days

def day_of_year(d): 

    # Assuming d is of the form yyyy-mm-dd

    year = d.split('-')[0]
    month = d.split('-')[1]
    day = d.split('-')[2]

    if int(day) > days_in_month(year, month):
        print 'Invalid date'
        return -1

    m = 1
    doy = 0

    while m < int(month): 
        doy = doy + days_in_month(year, str(m))
        m = m + 1

    return doy + int(day)

def days_from_base_year(base, d):
    
    # base is year of the form yyyy, d is of the form yyyy-mm-dd
    
    year = d.split('-')[0]
    month = d.split('-')[1]
    day = d.split('-')[2]

    y = int(base)
    dfb = 0

    while y < int(year): 
        dfb = dfb + days_in_year(y)
        y = y + 1

    return dfb + day_of_year(d)


def compare_dates(d1, d2): 
   
    # Assuming d1 and d2 are of the form yyyy-mm-dd, and d2 > d1

    d1_year = d1.split('-')[0]
    d1_month = d1.split('-')[1]
    d1_day = d1.split('-')[2]
    
    d2_year = d1.split('-')[0]
    d2_month = d1.split('-')[1]
    d2_day = d1.split('-')[2]

    days1 = days_from_base_year(d1_year, d1)
    days2 = days_from_base_year(d1_year, d2)

    return days2 - days1

def google_quote_time_format_convert(s):
    return datetime.datetime.strptime(s, '%d-%b-%y').strftime('%Y-%m-%d %H:%M:%S')

##############################################################################################
#
#    File read and write related functions
#
##############################################################################################

# ----------------------------------------------------------------
# read_master_data(): read master data file into dictionary object
# ----------------------------------------------------------------
def read_master_data():
    return json.loads(open(MASTER_DATA_FILE, 'r').read())

# ----------------------------------------------------------------
#  write_data(sym, data)
#  Dump data object to JSON file
# ----------------------------------------------------------------
def write_data(sym, data_object):
    filename = 'data/' + sym + '.json'
    j = json.dumps(data_object, indent=4)
    fp = open(filename, 'w')
    fp.write(j)
    fp.close()

# ----------------------------------------------------------------
#  Fill in default fields if not already in there
# ----------------------------------------------------------------
def setup_default_data(sym):

    data = {}

    if 'symbol' not in data.keys():
        data['symbol'] = sym

    if 'daily' not in data.keys():
        data['daily'] = []

    if 'weekly' not in data.keys():
        data['weekly'] = []

    if 'monthly' not in data.keys():
        data['monthly'] = []

    if 'dividend' not in data.keys():
        data['dividend'] = {}

    return data

# ----------------------------------------------------------------
#  read_data(sym)
#  If there is a file, read it in, otherwise, create a default 
#  data object to hold data.
# ----------------------------------------------------------------
def read_data(sym):
    filename = 'data/' + sym + '.json'
    if os.path.isfile(filename):
        data = json.loads(open(filename, 'r').read())
    else:
        # Don't have any data for the symbol, create a default one
        data = setup_default_data()

    return data

##############################################################################################
#
#    Tweet Files 
#
##############################################################################################

# ----------------------------------------------------------------
#  read_tweets(user)
#  Read tweets from json file for a user. Default is homeline
# ----------------------------------------------------------------
def read_tweets(user = 'homeline'):
    filename = 'data/' + user + '.json'
    if os.path.isfile(filename):
        return json.loads(open(filename, 'r').read())
    else:
        return None

# ----------------------------------------------------------------
#  write_tweets(user)
#  Dump tweet object to JSON file
# ----------------------------------------------------------------
def write_tweets(user, tweet_objects):
    filename = 'data/' + user + '.json'
    j = json.dumps(tweet_objects, indent=4)
    fp = open(filename, 'w')
    fp.write(j)
    fp.close()

##############################################################################################
#
#    Internet fectching related functions
#
##############################################################################################
def get_url_soup(url): 
    try:
        #print url
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        req = urllib2.Request(url, '', headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        return soup

    except urllib2.URLError as e:
        print 'Failed to open', url, 'because of', e.reason
        return None

def get_url_soup_no_user_agent(url):
    try:
        #print url
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        return soup

    except urllib2.URLError as e:
        print 'Failed to open', url, 'because of', e.reason
        return None

##############################################################################################
#
#    Symbol Files 
#
##############################################################################################
def gen_symbol_file():
    file1 = 'nasdaqlisted.txt'
    file2 = 'otherlisted.txt'
    symfile = 'data/' + 'symbols.txt'

    data1 = open(file1, 'r').read().split('\n')
    data2 = open(file2, 'r').read().split('\n')
    symbols = {}

    for line in data1[1:]:
        if len(line) > 0:
            ll = line.split('|')
            # Exclude test issues
            if ll[3] == 'N':
                 symbols[ll[0]] = ll[1]

    for line in data2[1:]:
        if len(line) > 0:
            ll = line.split('|')
            # Exclude test issues and use nasdaq symbols
            if ll[6] == 'N':
                symbols[ll[7]] = ll[1]

    j = json.dumps(symbols, indent=4)
    fp = open(symfile, 'w')
    fp.write(j)
    fp.close()

def load_symbols():
    symfile = 'data/' + 'symbols.txt'
    return json.loads(open(symfile, 'r').read())

def load_classification():
    classify_file_name = 'results/classify.json'
    if os.path.isfile(classify_file_name):
        classify = json.loads(open(classify_file_name, 'r').read())
    else:
        classify = {}
    return classify
    
def isfloat(a):
    try:
        float(a)
    except ValueError:
        return False

    return True

def isint(a):
    try:
        int(a)
    except ValueError:
        return False

    return True

def file_modification_time(filename):
    t_epoch = os.path.getmtime(filename)
    t_time_struct = time.gmtime(t_epoch)
    return t_time_struct.tm_year, t_time_struct.tm_mon, t_time_struct.tm_mday, t_time_struct.tm_wday
