import nltk
import os
import sys
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # dictionary for files
    files = dict()
    # implement filenames through directory
    filenames = os.listdir(directory)
    # loop through files in filenames
    for file in filenames:
        # implement path by joining file and directory
        path = os.path.join(directory, file)
        # open and read file
        with open(path, "r", encoding="utf-8") as f:
            # implement content as read files
            content = f.read()
        # cofirm files are in string format
        files[file] = str(content)
        
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # tokenize words
    words = nltk.word_tokenize(document)
    # implement stop word from nltk
    stop_word = nltk.corpus.stopwords.words("english")
    # empty list for results
    results = []
    # loop through words to check if stop word/ correct punctuation
    for word in words:
        if word not in stop_word and word not in string.punctuation:
            # if good to go, add word to results 
            results.append(word)
            
    return results


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # dict for idf's
    idf = dict()
    # empty list of words
    words = []
    # var for total
    total = len(documents)
    
    # loop through documents
    for document in documents:
        # loop through words in documnets and if not in document, add to words
        for word in documents.get(document):
            if word not in words:
                words.append(word)
    # loop through words
    for word in words:
        # initialize count
        count = 0
        # loop through documents for words in document and add to counter
        for document in documents:
            if word in documents.get(document):
                count += 1
        # calculate idf
        idf[word] = (math.log(total/count))
                    
    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # dictionary for scores
    scores = dict()
    # empty list for filenames
    filenames = []
    # loop through files
    for file in files:
        # empty list for tf-idf
        tf_idf = []
        # get words from files
        all_words = files.get(file)
        # loop through each query for words
        for word in query:
            # initialize frequency
            f = 0
            # loop through all_words
            for single_word in all_words:
                # make sure it is a word
                if single_word == word:
                    # add to frequency count if in all_words
                    f +=1
            # calculate and add to tf_idf list based on frequency and inverse frequency of word    
            tf_idf.append(f * idfs[word])
        # add files to scores dictionary with frequency score
        scores[file] = sum(tf_idf)
    # sort by highest score
    sort_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    # get as mmany scores as allowed by n
    for i in range(n):
        #add scores to filenames list as sorted scores   
        filenames.append(sort_scores[i][0])
        
    return filenames


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # empty list for final results
    results = []
    # dictionary for scores
    scores = dict()
    # loop through sentences
    for sentence in sentences:
        # empty list for inverse frequency
        idf = []
        # loop through words in sentences
        for word in sentences[sentence]:
            # loop through words in query
            for q_word in query:
                # check if same and add to idf list 
                if word == q_word:
                    idf.append(idfs[word])
            # matching word measure calculation for scores
            scores[sentence] = sum(idf)
    # sort by highest score
    sort_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    # get as many scores as allowed by n
    for i in range(n):
        #add scores to results list as sorted scores   
        results.append(sort_scores[i][0])
        
    return results

if __name__ == "__main__":
    main()
