import urllib
from bs4 import BeautifulSoup
import sys

url = 'https://twitter.com/FakeInfosecNews'

try:
    print "fetching %s" %url
    http = urllib.urlopen(url)
    if http.code != 200:
        raise TypeError('cannot fetch page: %s' %url)
    
    page = http.read()
    bs = BeautifulSoup(page, "lxml")
    
    i = 1
    for fake_tweet in bs.find_all('p', {'class': 'js-tweet-text'}):
        print "{0}. {1}".format(i, fake_tweet.string)
        i +=1
    
except TypeError, e:
    print >> sys.stdout, e
finally:
    sys.exit(0)