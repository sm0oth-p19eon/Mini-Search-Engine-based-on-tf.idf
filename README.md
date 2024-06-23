# Mini Search Engine Project based on tf.idf score

## Overview

This project involves implementing a variant of the Vector Space retrieval model for a search engine. The Vector Space model represents documents as vectors where each dimension corresponds to a term from the vocabulary, and the values are term frequencies (tf).

## Key Concepts

### Vector Space Model
- **Documents as Bag of Words**: Documents are considered as collections of words without regard to order or syntax.
- **Term Frequency (tf)**: Measures how often a word occurs in a document.
- **Inverse Document Frequency (idf)**: Indicates how informative a term is across all documents.

### tf.idf Weighting Scheme
- **tf.idf Weight**: The product of term frequency (tf) and inverse document frequency (idf). This weight represents the importance of a term within a document relative to all documents.
- **Sparse Vectors**: Document and query vectors are sparse, containing many zeros due to terms appearing in only a few documents or queries.

### Cosine Similarity
- **Relevance Calculation**: The relevance of a document to a query is calculated using cosine similarity, which measures the angle between the document and query vectors. A cosine similarity of 1 indicates maximum relevance.

## Implementation Details

1. **Term Frequency Calculation**: Compute term frequencies for each term in the documents.
2. **Inverse Document Frequency Calculation**: Compute idf for each term across all documents.
3. **Vector Representation**: Represent documents and queries as vectors of tf.idf values.
4. **Cosine Similarity**: Calculate the cosine similarity between document and query vectors to determine relevance.

## Usage

```
$ py SearchEngine.py [-arg1] [-arg2]
```

arg1 is the name of the source document collection. arg2 is a flag indicating wether to create a new index or use existing indices.

## Disclaimer

This is a course project. The module stemming is provided by the professor.