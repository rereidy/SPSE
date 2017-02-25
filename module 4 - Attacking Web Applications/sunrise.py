import urllib2
from bs4 import BeautifulSoup

soup = BeautifulSoup(urllib2.urlopen('http://www.timeanddate.com/worldclock/astronomy.html?n=75').read())

for row in soup('table', {'class' : 'spad'})[0].tbody('tr'):
    tds = row('td')
    print tds[0].string, tds[1].string, tds[5].string, tds[7].string