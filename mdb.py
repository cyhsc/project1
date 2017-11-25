import sys
from pymongo import MongoClient
from pprint import pprint

def test(): 

    client = MongoClient('localhost')
    print client.database_names()
    movie_db = client['movie']
    collections = movie_db.collection_names(include_system_collections=False)
    print collections
    gc = movie_db['gangster']
    sfc = movie_db['science_fiction']

    result = gc.find_one({'name': 'Once upon a time in America'})
    if result == None:
        gc.insert_one({'name': 'Once upon a time in America'})

    cursor = gc.find()
    for document in cursor:
        print document

    print 'Trying to find the document'
    result = gc.find_one({'name': 'Once upon a time in America'})
    print result

    print 'Now delete the document'

    gc.find_one_and_delete({'name': 'Once upon a time in America'})

    cursor = gc.find()
    for document in cursor:
        print document

def main(argv):
    test()

if __name__ == '__main__':
    main(sys.argv[1:])
