import re
import sys
import os.path
import urllib2
import urllib
import random

from bs4 import BeautifulSoup



#url = 'http://www.musigh.com/page/{0}'.format(n)


def main():
    mp3list = []
    links = makelinks()
    mp3list = getmp3(links)
    download(mp3list)

def download(mp3list):
    n=0
    for link in mp3list:
        n = n + 1
        name = link.split("/")[-1]
        if os.path.exists(name): #Filnavnet
            print "File {0} of {1} exits".format(n,len(mp3list))
            continue
        try:
            print "Downloading {0} of {1}".format(n,len(mp3list))
            urllib.urlretrieve(link, name)
        except urllib.ContentTooShortError:
            print "File too small"
        else:
            continue
        
def getmp3(links):
    mp3list = []
    n = 0
    for page in links:
        n = n + 1 
        try:
            pagedata = urllib2.urlopen(page).read()
            soup = BeautifulSoup(pagedata)
            if soup == None:
                    continue
            else:
                oldlen = len(mp3list)
                for mp3 in soup.find_all("a", href = re.compile("^.*\.mp3$")):
                    mp3list.append(mp3["href"])
                print "Page: {0}: {1} new links found! Total: {2}".format(n,len(mp3list)-oldlen, len(mp3list))
        except urllib2.HTTPError:
            print "No more pages to be read"
            break
    return mp3list



def makelinks():
    links = []
    for n in range(0,200):
        links.append('http://www.musigh.com/page/{0}'.format(n))
    return links   


if __name__ == "__main__":
    main()
