import sys

def main(argv):

    filename = argv[0]
    print 'Reading file', filename

    line = open(filename, 'r').read().split('\n')[0]
    print line
    symbols = line.split()

    f = open(filename, 'w')
    for sym in symbols:
        f.write(sym.lstrip('$') + '\n')

if __name__ == '__main__':
    main(sys.argv[1:])
