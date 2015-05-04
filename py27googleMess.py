#!/usr/bin/env python2.7
import mechanize
import re
import codecs
from random import randint, choice
from collections import defaultdict
from time import sleep
import sys
import string
from optparse import OptionParser


def searchGoogle(Browser, url):

    links = []
    Browser.open(url)

    try:
        for link in Browser.links():
            if re.search(r'(\w+\s+){3,}', link.text): # to exclude images or other things that have no clear description (in words) towards the user
                links.append(link)
    except:
        sys.stderr.write('ERROR: Failed to retrieve search results.\n')
        sys.exit(1)

    return links


def visitLinks(Browser, links, nrOfLinksToClick):

    for j in range(nrOfLinksToClick):
        link = links[randint(0, len(links))]
        sys.stderr.write('INFO: Visited %s\n' % link.url)
        sleepInt = randint(2, 15)
        sys.stderr.write('INFO: Going to sleep now for %i seconds.\n' % sleepInt)
        sleep(sleepInt)# sleep in seconds
        try:
            response = Browser.follow_link(link)
        except:
              sys.stderr.write('ERROR: Failed to follow link.\n')
              sys.exit(1)


def selectRandomNgram(fh):

    fileLines = fh.readlines()
    lines = []
    ngramDict = defaultdict(int)
    # Note: analyzing each line and populating a complete ngramDict is far from elegant. But when randomly selecting a line from the corpus and extracting some ngrams from that, there is a risk of selecting empty/short lines. Which needed quite some lines to work around. Plus, this isn't exactly going to be a performance bottle neck.
    
    for line in fileLines:
        line = line.strip()
        if line:
            raw = re.sub(r'\W', ' ', line)
            tokens = raw.split()
            ngramLength = randint(0, min(len(tokens)-1, 5))
            n = ngrams(tokens, ngramLength)
            for ngram in n:
                ngramDict[tuple(ngram)] += 1
    
    return choice(ngramDict.keys())
    

def ngrams(tokens, ngramLength):

    n = []
    for i in range(len(tokens)-ngramLength):
        n.append(tokens[i:i+ngramLength])
    return n


if __name__ == '__main__':
    
    parser = OptionParser("usage: %prog corpus")
    parser.add_option("-t", "--textFile", dest="textFile", help="Specify text file to read from, selecting some random ngrams")
    options, args = parser.parse_args()

    if not options.textFile:
        parser.print_help(sys.stderr)
        sys.exit(1)

    ngram = selectRandomNgram(codecs.open(options.textFile, 'r', 'utf-8'))

    # go to http://whatsmyuseragent.com/ to get the user agent string of your own browser
    userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'

    # make getURL for this
    url = 'http://www.google.com/search?q=%s&num=100&hl=en&start=0' % '+'.join(ngram)
    sys.stderr.write('INFO: Querying "%s"\n' % ' '.join(ngram))

    Browser = mechanize.Browser()
    #Browser.set_all_readonly(False)
    Browser.set_handle_robots(False)
    Browser.set_handle_refresh(False)
    Browser.addheaders = [('User-agent', userAgent)]


    nrOfLinksToClick = randint(2,8)

    links = searchGoogle(Browser, url)

    visitLinks(Browser, links, nrOfLinksToClick)
    

        
    
