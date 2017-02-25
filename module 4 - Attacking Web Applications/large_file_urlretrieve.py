from urllib import urlretrieve
import sys
import getopt
from os.path import exists, normpath, sep

DEFAULT_FILE_LOC    = '.'

class DownloadFile(object):
    def __init__(self, site, location=DEFAULT_FILE_LOC, filename=None):
        self.__url__      = site
        self.__location__ = location
        if filename is not None:
            self.filename = normpath("{0}{1}{2}".format(self.__location__, sep, filename))
        else:
            self.filename = normpath("{0}{1}{2}".format(self.__location__, sep, self.__url__.split(sep)[-1]))

    def textprogress(self, count, blockSize, totalSize):    
        try:
            frac = float(count*blockSize)/float(totalSize)
        except:
            frac = 0
        
        bar = "=" * int(25*frac)
        
        sys.stdout.write("\r%-25.25s %3i%% |%-25.25s| %5sB of %5sB" %
            (self.filename,
             frac*100,
             bar,
             self.format_number(count*blockSize),
             self.format_number(float(totalSize))))
        sys.stdout.flush()
        
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

    def perform(self):
        try:
            urlretrieve(self.__url__, self.filename, reporthook=self.textprogress)
        except KeyboardInterrupt:
            raise
        finally:
            sys.stdout.write("\n")

def process_args(args):
    url= None
    loc = DEFAULT_FILE_LOC
    
    try:
        opts, args = getopt.getopt(args, 'hu:o:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-u':
                url = arg
            elif opt == '-o':
                loc = arg
    except TypeError:
        raise
    except getopt.GetoptError:
        raise('invalid argument')
    
    return (url, loc)

def usage():
    print >> sys.stderr, """
{0} - large file download & monitor
usage: {0} -u url -o download_location [-h]
""".format(sys.argv[0])

if __name__ == "__main__":
    try:
        (url, loc) = process_args(sys.argv[1:])
        if url is None or loc is None:
            raise TypeError('missing arguments')
        elif not exists(loc):
                raise('output directory does not exist')
        
        f = DownloadFile(site=url, location=loc)
        f.perform()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        print "download interrupted"
        sys.exit(0)
    except (TypeError, IOError, getopt.GetoptError), e:
        print >> sys.stderr, e
        usage()
        sys.exit(1)
    else:
        print "{0} download complete".format(f.filename)
        sys.exit(0)