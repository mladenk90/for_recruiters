import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# CF grammar for NonTerminals
NONTERMINALS = """
S -> NP VP | VP NP | S Conj S | S NP | S P NP | S P S 
NP -> N | Det N | NP PP | Det A N | NP Adv V | A N | P NP | Det N A | Det A N
VP -> V | V NP | V P NP | V A | V P
A -> Adj | adj A | Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenize words
    words = nltk.word_tokenize(sentence)
    # dict for total
    total = []
    # loop through words
    for word in words:
        # initialize word count
        word_count = 0
        # loop through characters in word and check if capital letters and add to word count
        for s in word:
            if s.isalpha():
                word_count += 1
        # if all lower case then add to words        
        if word_count > 0:    
            total.append(word.lower())
                
    return total    


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    # list for chunnk
    chunk = []
    # loop through all subtrees and check for NP label
    for t in tree.subtrees():
        if t.label() == "NP":
            # initialize counter
            counter = 0
            # loop through NP labels and subtrees
            for np in t.subtrees():
                # if NP in label add to count
                if np.label == "NP":
                    counter += 1
            # check if counter on last NP and add to chunk
            if counter == 1:
                chunk.append(t)
    return chunk
      
    


if __name__ == "__main__":
    main()
