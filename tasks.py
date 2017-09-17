import sys
from tweets import Tweets

def update_tweets():
    t = Tweets()
    t.update()
    t.process()

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

if __name__ == '__main__':
    main(sys.argv[1:])
