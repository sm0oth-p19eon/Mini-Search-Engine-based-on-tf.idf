
from DocParser import *
from Indexer import *


class Query:
    
    def __init__(self, querylist, indexer: Indexer) -> None:
        self.vocab = {}
        self.max_ocurr = 0
        self.indexer = indexer
        self.tfidf = {}
        self.executable = False

        for token in querylist:
            processed_list = stem_tokenize(token)
            for processed in processed_list:
                if processed in indexer.idf_index.keys():
                    self.executable |= True
                vocab_add(processed, self.vocab)
                if self.vocab[processed]['total'] > self.max_ocurr:
                    self.max_ocurr = self.vocab[processed]['total']

        if self.executable:
            self.tf = {}

            for word, freq in self.vocab.items():
                self.tf[word] = freq['total']/self.max_ocurr

            idf = self.indexer.idf_index

            for word, tf in self.tf.items():
                if word in idf.keys():
                    self.tfidf[word] = tf * idf[word]

            for word, idf in idf.items():
                if word not in self.tfidf.keys():
                    self.tfidf[word] = 0

            temp_sum = 0
            for word, score in self.tfidf.items():
                temp_sum += score ** 2

            self.magnitude = math.sqrt(temp_sum)