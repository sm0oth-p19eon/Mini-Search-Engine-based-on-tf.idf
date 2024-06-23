
from stemming.porter2 import stem
import string
import xml.etree.ElementTree
from Indexer import *
from DocParser import *
from Query import *
import sys


class SearchEngine:

    def __init__(self, collection_name, create):
        """
        Initialize the search engine, i.e. create or read in index. If
        create=True, the search index should be created and written to
        files. If create=False, the search index should be read from
        the files. The collection_name points to the filename of the
        document collection (without the .xml at the end). Hence, you
        can read the documents from <collection_name>.xml, and should
        write / read the idf index to / from <collection_name>.idf, and
        the tf index to / from <collection_name>.tf respectively. All
        of these files must reside in the same folder as THIS file.
        """
        if create:
            print('Creating index...')
            collection = Doc_collection(collection_name)
            collection.print_idf()
            collection.print_tf()
        
        self.indexer = Indexer(collection_name)

        print('Done.')

    def execute_query(self, query_terms):
        """
        Input to this function: List of query terms

        Returns the 10 highest ranked documents together with their
        tf.idf scores, sorted by score. For instance,

        May be less than 10 documents if there aren't as many documents
        that contain the terms.
        """
        query_doc = Query(query_terms, self.indexer)
        if not query_doc.executable:
            return 1
        
        results = self.indexer.compare(query_doc.magnitude, query_doc.tfidf)
        return results

    def execute_query_console(self):
        """
        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        """
        query_input = input('Please enter query, terms seperated by whitespace:')
        if len(query_input)== 0:
            return 1
        query_input_list = query_input.split()
        query_result = self.execute_query(query_input_list)
        if query_result == 1:
            print('No result found for the given terms.')
            return 0
        print('I found the follwing documents:')
        for doc, score in query_result:
            print(doc + '\t' + '(' + str(score) + ')')
        return 0

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        raise Exception('Invalid number of options. (expected 2)')
    
    collection = sys.argv[1]
    create = sys.argv[2]

    if create not in ['t', 'f']:
        raise Exception('Invalid create option. Enter t for true, f for false.')
    
    boolean_map = {'t': True, 'f': False}
    
    search_engine = SearchEngine(collection_name=collection, create=boolean_map[create])
    while True:
        if(search_engine.execute_query_console()):
            break

