#!/usr/bin/env python

import urllib
from bs4 import BeautifulSoup

url = 'http://resources.infosecinstitute.com/category/hacking-2/'

def main():
    print "Scraping url: %s" % url
    httpResponse = urllib.urlopen(url)
    print "Code: %s" % httpResponse.code
    html = httpResponse.read()
    bs = BeautifulSoup(html, 'lxml')
    section = bs.find('div', {'id' : 'items-wrapper'})
    links = section.find_all('div', {'class' : 'item-thumb'})
    for link in links:
        articlelink = link.find('a')
        # print articlelink
        title = articlelink['title']
        urllink = articlelink['href']
        print "\nTitle: %s" % title
        print "Link: %s" % urllink

if __name__ == '__main__':
    main()