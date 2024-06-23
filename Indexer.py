
import xml.etree.ElementTree as ET
from stemming.porter2 import stem
from DocParser import *
import math

class Indexer:

    def __init__(self, collection_name) -> None:
        print('Reading index from file...')
        idf_filepath = collection_name + '.idf'
        tf_filepath = collection_name + '.tf'
        self.idf_index = {}
        with open(idf_filepath) as idf_f:
            for line in idf_f:
                word, idf = line.split('\t')
                self.idf_index[word] = float(idf)

        self.tf_index = {}
        with open(tf_filepath) as tf_f:
            for line in tf_f:
                doc, word, tf = line.split('\t')
                if doc not in self.tf_index.keys():
                    self.tf_index[doc] = {}
                    self.tf_index[doc][word] = float(tf)
                else:
                    self.tf_index[doc][word] = float(tf)

        self.tfidf_index = {}
        self.magnitude_index = {}

        for doc, word_tf in self.tf_index.items():
            if doc not in self.tfidf_index.keys():
                self.tfidf_index[doc] = {}
            for word, tf in word_tf.items():
                self.tfidf_index[doc][word] = tf * self.idf_index[word]
            for word, idf in self.idf_index.items():
                if word not in self.tfidf_index[doc].keys():
                    self.tfidf_index[doc][word] = 0

    
    def compare(self, query_magnitude, query_tfidf):
        result = {}
        result_list = []
        for doc, vector in self.tfidf_index.items():
            temp_sum = 0
            for word, score in self.tfidf_index[doc].items():
                temp_sum += score ** 2
            doc_magnitude = math.sqrt(temp_sum)
            dot_product = 0
            for word, score in query_tfidf.items():
                dot_product += score * self.tfidf_index[doc][word]
            result[doc] = dot_product/(query_magnitude*doc_magnitude)
        
        sorted_keys = iter(sorted(result, key=result.get, reverse=True))
        i = 0
        while i < 10:
            doc = next(sorted_keys)
            if result[doc] != 0:
                result_list.append((doc, result[doc]))
            i += 1

        return result_list


