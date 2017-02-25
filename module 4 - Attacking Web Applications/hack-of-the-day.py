from bs4 import BeautifulSoup
import urllib
import sys

try:
    http = urllib.urlopen('http://www.securitytube.net/user/Hack-of-the-Day')
    if http.code != 200:
        raise TypeError('error getting page: {0}'.format(http.code))
    soup = BeautifulSoup(http.read(), 'lxml')
    
    for links in soup.find_all('div'):
        print links

    recent = soup.find_all('li', attrs={'a': 'href'})
    if recent is None:
        raise TypeError('cannot find tag \'ul\' with attribute of \'list-of-vuls\'')

    lis = recent.find_all('li')

    for vul in lis:
        vul_date = vul.find('span', 'vul-date').string
        vul_id = vul.find('span', 'vul-id').string
        vul_title = vul.find('span', 'vul-title').string

    print "{0} ({1}) - {2}".format(vul_id, vul_date, vul_title)
    
except TypeError, e:
    print >> sys.stderr, e
    sys.exit(1)
    
sys.exit(0)