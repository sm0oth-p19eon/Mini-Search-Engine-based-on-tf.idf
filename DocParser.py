
import math
import xml.etree.ElementTree as ET
import string
from stemming.porter2 import stem

'''
    A helper function to add all the stemmed words into a vocabulary
    for a single doc.
'''
def vocab_add(word, vocab: dict):
    if word in vocab:
        vocab[word]['total'] += 1
    else:
        vocab[word] = {'total': 1, 'n_of_docs': 1}


'''
    A helper function to tokenize a piece of text content.
'''
def stem_tokenize(content):
    stemmed = []
    raw_tokens = content.lower().split()
    for token in raw_tokens:
        for character in token:
            if character in string.punctuation:
                token = token.replace(character, '')
        if token != '':
            stemmed.append(stem(token)) 
    return stemmed


'''
    A function to extract vocabulary from a doc element.
'''
def get_doc_vocab(doc):
    vocab = {}
    max_ocurr = 0

    for headline in doc.iter('HEADLINE'):
        stemmed_tokens = stem_tokenize(headline.text)
        for word in stemmed_tokens:
            vocab_add(word, vocab)
            if vocab[word]['total'] > max_ocurr:
                max_ocurr = vocab[word]['total']

    for paragraph in doc.iter('P'):
        stemmed_tokens = stem_tokenize(paragraph.text)
        for word in stemmed_tokens:
            vocab_add(word, vocab)
            if vocab[word]['total'] > max_ocurr:
                max_ocurr = vocab[word]['total']

    return vocab, max_ocurr


'''
    A function to retrieve the id of a single doc element.
'''
def get_doc_id(doc):
    return doc.attrib['id']


'''
    A class representing a single doc of text.
'''
class Doc:

    def __init__(self, doc_element) -> None:
        self.id = get_doc_id(doc_element)
        v, m = get_doc_vocab(doc_element)
        self.vocab = dict(sorted(v.items()))
        self.max_ocurr = m


    def print_tf(self, f):
        for word, freq in self.vocab.items():
            print(self.id + '\t' + word + '\t' + str(freq['total']/self.max_ocurr), file=f)



'''
    A class representing a collection of texts.
'''
class Doc_collection:

    def __init__(self, collection_name) -> None:
        self.collection_name = collection_name
        self.tree = ET.parse('DocumentCollections/' + self.collection_name + '.xml')
        self.root = self.tree.getroot()
        self.docs = {}
        self.combined_vocab = {}
        for d in self.root:
            doc_obj = Doc(d)
            self.docs[doc_obj.id] = doc_obj
            for word, freq in doc_obj.vocab.items():
                if word in self.combined_vocab.keys():
                    self.combined_vocab[word]['total'] += freq['total']
                    self.combined_vocab[word]['n_of_docs'] += 1
                else:
                    self.combined_vocab[word] = freq
        self.combined_vocab = dict(sorted(self.combined_vocab.items()))
        self.n_of_docs = len(self.docs)

    def print_idf(self):
        with open(self.collection_name + '.idf', 'w+') as idf_file:
            for word, freq in self.combined_vocab.items():
                line = word + '\t' + str(math.log(self.n_of_docs/freq['n_of_docs'])) + "\n"
                idf_file.write(line)


    def print_tf(self):
        with open(self.collection_name + '.tf', 'w+') as tf_file:
            for doc in self.docs.values():
                doc.print_tf(tf_file)
                
