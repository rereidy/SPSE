import pycurl
import sys
import getopt
from os.path import exists, normpath, sep, getsize

DEFAULT_FILE_LOC    = '.'

class DownloadFile(object):
    def __init__(self, proxy=None):
        self.crl = pycurl.Curl()
        self.crl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.crl.setopt(pycurl.MAXREDIRS,      5)
        self.crl.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.crl.setopt(pycurl.AUTOREFERER,    1)
        
    def perform(self, url, output_dir=DEFAULT_FILE_LOC, filename=None, resume=True, progress=None):
        
        # Generate filename if not given
        if not filename:
            filename = normpath("{0}{1}{2}".format(output_dir, sep, url.strip("/").split("/")[-1].strip())) 
        self.filename = filename
 
        # Get resume information
        self.existing = self.start_existing = 0
        if resume and exists(filename):
            self.existing = self.start_existing = getsize(filename)
            self.crl.setopt(pycurl.RESUME_FROM, self.existing)
 
        # Configure progress hook            
        if progress:
            self.crl.setopt(pycurl.NOPROGRESS,       0)
            self.crl.setopt(pycurl.PROGRESSFUNCTION, progress)
            
        # Configure url and destination
        self.crl.setopt(pycurl.URL, url)
        self.crl.setopt(pycurl.WRITEDATA, open(filename, "ab"))
        
        # Start
        self.crl.perform()
        
        sys.stdout.write("\n")

    def format_number(self, number, SI=0, space=' '):
        """Turn numbers into human-readable metric-like numbers"""
        symbols = ['',  # (none)
                   'k', # kilo
                   'M', # mega
                   'G', # giga
                   'T', # tera
                   'P', # peta
                   'E', # exa
                   'Z', # zetta
                   'Y'] # yotta
    
        if SI: 
            step = 1000.0
        else: 
            step = 1024.0
 
        thresh = 999
        depth = 0
        max_depth = len(symbols) - 1
    
        # we want numbers between 0 and thresh, but don't exceed the length
        # of our list.  In that event, the formatting will be screwed up,
        # but it'll still show the right number.
        while number > thresh and depth < max_depth:
            depth  = depth + 1
            number = number / step
 
        if type(number) == type(1) or type(number) == type(1L):
            # it's an int or a long, which means it didn't get divided,
            # which means it's already short enough
            fmt = '%i%s%s'
        elif number < 9.95:
            # must use 9.95 for proper sizing.  For example, 9.99 will be
            # rounded to 10.0 with the .1f format string (which is too long)
            fmt = '%.1f%s%s'
        else:
            fmt = '%.0f%s%s'
        
        return(fmt % (float(number or 0), space, symbols[depth]))

    def textprogress(self, download_t, download_d, upload_t, upload_d):            
        downloaded = download_d + self.existing
        total      = download_t + self.start_existing
        try:
            frac = float(downloaded)/float(total)
        except:
            frac = 0
        
        bar = "=" * int(25*frac)
        
        sys.stdout.write("\r%-25.25s %3i%% |%-25.25s| %5sB of %5sB" %
            (self.filename,
             frac*100,
             bar,
             self.format_number(downloaded),
             self.format_number(total)))
        sys.stdout.flush()

def process_args(args):
    url               = None
    download_location = DEFAULT_FILE_LOC
    
    try:
        opts, args = getopt.getopt(args, 'hu:o:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-u':
                url = arg
            elif opt == '-o':
                download_location = arg
    except TypeError:
        raise
    except getopt.GetoptError:
        raise('invalid argument')
    
    return (url, download_location)

def usage():
    print >> sys.stderr, """
{0} - large file download & monitor
usage: {0} -u url -o download_location [-h]
""".format(sys.argv[0])

if __name__ == "__main__":
    try:
        (url, location) = process_args(sys.argv[1:])
        if url is None or location is None:
            raise TypeError('missing arguments')
        elif not exists(location):
                raise('output directory does not exist')
        
        f = DownloadFile()
        f.perform(url, output_dir=location, progress=f.textprogress)
    except pycurl.error, e:
        print >> sys.stderr, e
        sys.exit(1)
    except (TypeError, IOError, getopt.GetoptError), e:
        print >> sys.stderr, e
        usage()
        sys.exit(1)
    else:
        print "{0} download complete".format(f.filename)
        sys.exit(0)
    