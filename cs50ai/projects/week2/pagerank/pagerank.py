import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # dictionary for probability distribution
    probability_dist = dict()
    
    # With probability `damping_factor`, choose a link at random linked to by `page`
    page_link = corpus[page]
    
    #With probability `1 - damping_factor`, choose a link at random chosen from all pages in the corpus
    # var  for list of available links
    available_link = []
    # check if page in corpus and add to available_link
    for page in corpus:
        available_link.append(page)
        # initialize probability dist via page
        probability_dist[page] = 0
    # check if link in page_link
    for link in page_link:
        # apply damping factor for page_link
        probability_dist[link] = (damping_factor) * (1/len(page_link))
    # check if link in available_link
    for link in available_link:
        # apply damping factor for available_link
        probability_dist[link] = probability_dist[link] + ((1- damping_factor) * (1/len(available_link)))
    
    return probability_dist
        
    
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # get pages from corpus key/value pairs in dictionary in a list
    pages = list(corpus.keys())
    # dictionary for new pages
    new_pages = dict()
    # random initial page
    initial_page = random.choice(pages)
    # go through each page in pages and initialize probablitiy dist to 0
    for page in pages:
        new_pages[page] = 0
    # Update probablity via N samples from previous pages(initial page)
    new_probablity = transition_model(corpus, initial_page, damping_factor)
    # go through new probablities via new sample from initial page
    for i in range(0, n-1):
        # random page based on new probablity applied via key/value pairs
        random_page = random.choices(list(new_probablity.keys()), list(new_probablity.values()))
        # add probablity of page popping up randomly via new sample
        new_pages[random_page[0]] = new_pages[random_page[0]] + 1/n
        # get new updated probabity via transition model
        new_probablity = transition_model(corpus, random_page[0], damping_factor)
        
    return new_pages
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # dictionary for total number of links
    numlinks = dict()
    # dictionary for page
    page = dict()
    # set variable for corpus length    
    n = len(corpus)
    # set variable for damping factor   
    d = damping_factor
    # dictionary for pagerank
    pagerank = dict()
    # loop through selected corpus set
    for i in corpus:
        pagerank[i] = set()
        # confirm ready to initialize
        if (len(corpus[i]) == 0):
            corpus[i] = set(corpus.keys())
    # get page and page rank from dictionary via key:value pairs    
    for i in corpus:
        for j in corpus[i]:
            pagerank[j].add(i)
        numlinks[i] = len(corpus[i])
    
    # initialize page
    for i in corpus:
        page[i] = 1/n
    
    
    while True:
        # dictionary for new pages
        new_page = dict()
        # loop through and apply damping factor/sample for page
        for i in corpus:
            new_page[i] = (1 - d) / n
            # loop through and apply damping factor/sample for pagerank
            for j in pagerank[i]:
                new_page[i] += d * page[j] / numlinks[j]
                
        # var for active
        active = True
        if active:
            # loop through to check for difference in sample and iteration
            for i in corpus:
                diff = abs(new_page[i] - page[i])
                # limit difference to .001
                if diff >= .001:
                    active = False
                # compare difference and update to sample
                page[i] = new_page[i]        
            # end iteration if udner .001          
            if active:
                break                           
    return page

if __name__ == "__main__":
    main()
